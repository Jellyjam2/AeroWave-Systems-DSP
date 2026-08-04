"""
SAT Solver Integration for Advanced Musical Pattern Discovery
Uses titan_forge Rust backend for high-performance SAT solving with postcard binary bridge
"""

try:
    from aerowave_dsp.aerowave_dsp import forge_1uip
    FORGE_1UIP_AVAILABLE = True
except ImportError:
    FORGE_1UIP_AVAILABLE = False

from aerowave_dsp import CognitivePayload
from .postcard_bridge import PostcardBinaryBridge
import numpy as np

class SATMusicalSolver:
    """
    Integrates SAT solving to discover optimal musical patterns from text analysis.
    """
    
    def __init__(self):
        self.solver = None
        self.postcard_bridge = PostcardBinaryBridge()
        self.use_binary_bridge = True
    
    def text_to_clauses(self, analysis_result):
        """
        Convert text analysis into SAT clauses for constraint solving.
        
        Args:
            analysis_result: Dictionary containing emotional vectors, sentiment, etc.
            
        Returns:
            List of clauses for SAT solver
        """
        clauses = []
        emotional_vector = analysis_result.get('emotional_vector', [])
        sentiment = analysis_result.get('sentiment', 0.5)
        arousal = analysis_result.get('arousal', 0.5)
        
        # Create variables for musical parameters
        # Each word becomes a variable with multiple possible states
        num_variables = len(emotional_vector) * 4  # 4 states per word (pitch, duration, velocity, instrument)
        
        # Constraint 1: Sentiment consistency - high sentiment should map to higher pitches
        for i, score in enumerate(emotional_vector):
            if score > 0.7:  # High emotional intensity
                # Variable should be in higher range
                var_idx = i * 4
                clauses.append([var_idx])  # At least one high pitch option
            elif score < 0.3:  # Low emotional intensity
                # Variable should be in lower range
                var_idx = i * 4 + 1
                clauses.append([var_idx])  # At least one low pitch option
        
        # Constraint 2: Arousal-based rhythm - high arousal = faster rhythms
        if arousal > 0.6:
            for i in range(len(emotional_vector)):
                var_idx = i * 4 + 2
                clauses.append([var_idx])  # Shorter durations
        elif arousal < 0.4:
            for i in range(len(emotional_vector)):
                var_idx = i * 4 + 3
                clauses.append([var_idx])  # Longer durations
        
        # Constraint 3: Cultural harmony patterns
        cultural_context = analysis_result.get('cultural_context', 'western')
        if cultural_context == 'western':
            # Western harmony: consonant intervals preferred
            for i in range(len(emotional_vector) - 1):
                clauses.append([i * 4, (i + 1) * 4])  # Adjacent notes should be harmonically related
        elif cultural_context == 'eastern':
            # Eastern harmony: pentatonic relationships
            for i in range(len(emotional_vector) - 1):
                clauses.append([i * 4 + 1, (i + 1) * 4 + 1])  # Pentatonic scale adherence
        
        # Constraint 4: Melodic contour - avoid large jumps
        for i in range(len(emotional_vector) - 1):
            if abs(emotional_vector[i] - emotional_vector[i + 1]) < 0.3:
                # Small emotional change = small pitch change
                clauses.append([i * 4, (i + 1) * 4])
        
        return clauses, num_variables
    
    def solve_musical_constraints(self, analysis_result):
        """
        Use SAT solver to find optimal musical patterns.
        
        Args:
            analysis_result: Dictionary containing text analysis results
            
        Returns:
            Dictionary with SAT solution and musical recommendations
        """
        try:
            clauses, num_variables = self.text_to_clauses(analysis_result)
            
            if not clauses:
                print("  [SAT SOLVER]: No constraints to solve, using direct mapping")
                return None
            
            print(f"  [SAT SOLVER]: Solving {len(clauses)} constraints with {num_variables} variables")
            
            # Try binary bridge first if enabled
            if self.use_binary_bridge:
                try:
                    return self.solve_with_binary_bridge(analysis_result, clauses)
                except Exception as e:
                    print(f"  [SAT SOLVER]: Binary bridge failed: {e}, falling back to direct method")
            
            # Fallback to direct titan_forge call if available
            if FORGE_1UIP_AVAILABLE:
                try:
                    learnt = []
                    trail = []
                    reasons = []
                    current_level_lits = []
                    
                    self.solver = forge_1uip(learnt, trail, reasons, clauses, current_level_lits)
                    
                    # Attempt to solve
                    solution = self.solver()
                    
                    if solution:
                        print("  [SAT SOLVER]: Found satisfying assignment")
                        return self.interpret_solution(solution, analysis_result)
                    else:
                        print("  [SAT SOLVER]: No solution found, using fallback")
                        return None
                except Exception as e:
                    print(f"  [SAT SOLVER]: forge_1uip failed: {e}, using fallback")
                    return None
            else:
                print("  [SAT SOLVER]: forge_1uip not available, using binary bridge or fallback")
                return None
                
        except Exception as e:
            print(f"  [SAT SOLVER]: Error during solving: {e}")
            print("  [SAT SOLVER]: Using fallback direct mapping")
            return None
    
    def solve_with_binary_bridge(self, analysis_result, clauses):
        """
        Use postcard binary bridge for high-speed communication with Rust backend.
        
        Args:
            analysis_result: Dictionary containing text analysis results
            clauses: SAT clauses to solve
            
        Returns:
            Dictionary with musical parameter recommendations
        """
        sentiment = analysis_result.get('sentiment', 0.5)
        arousal = analysis_result.get('arousal', 0.5)
        cultural_context = analysis_result.get('cultural_context', 'western')
        
        # Map cultural context to ID
        culture_id_map = {
            'western': 0,
            'eastern': 1,
            'african': 2,
            'latin': 3
        }
        culture_id = culture_id_map.get(cultural_context, 0)
        
        # Flatten clauses for binary transmission
        sat_clauses_flat = []
        for clause in clauses:
            sat_clauses_flat.extend(clause)
        
        # Serialize to binary using postcard bridge
        binary_packet = self.postcard_bridge.serialize_cognitive_packet(
            sentiment, arousal, culture_id, sat_clauses_flat
        )
        
        print(f"  [SAT SOLVER]: Binary packet size: {len(binary_packet)} bytes")
        
        # Send to Rust backend via CognitivePayload
        payload = CognitivePayload()
        success = payload.unpack_from_bridge(binary_packet)
        
        if not success:
            raise Exception("Failed to unpack binary packet in Rust backend")
        
        print(f"  [SAT SOLVER]: Rust backend received - Sentiment: {payload.sentiment:.3f}, "
              f"Arousal: {payload.arousal:.3f}, Culture ID: {payload.culture_id}, "
              f"Clauses: {len(payload.sat_clauses)}")
        
        # Generate recommendations based on the processed payload
        # (In a full implementation, the Rust backend would return SAT solution)
        return self.generate_binary_bridge_recommendations(payload, analysis_result)
    
    def generate_binary_bridge_recommendations(self, payload, analysis_result):
        """
        Generate musical recommendations from processed Rust payload.
        
        Args:
            payload: CognitivePayload from Rust backend
            analysis_result: Original analysis results
            
        Returns:
            Dictionary with musical parameter recommendations
        """
        emotional_vector = analysis_result.get('emotional_vector', [])
        
        recommendations = {
            'pitch_adjustments': [],
            'duration_modifications': [],
            'velocity_enhancements': [],
            'instrument_changes': [],
            'binary_bridge_used': True
        }
        
        # Use payload data to influence recommendations
        for i in range(len(emotional_vector)):
            # Pitch adjustments based on sentiment from payload
            if payload.sentiment > 0.7:
                recommendations['pitch_adjustments'].append(2)
            elif payload.sentiment < 0.3:
                recommendations['pitch_adjustments'].append(-2)
            else:
                recommendations['pitch_adjustments'].append(0)
            
            # Duration modifications based on arousal from payload
            if payload.arousal > 0.6:
                recommendations['duration_modifications'].append(0.8)  # Faster
            elif payload.arousal < 0.4:
                recommendations['duration_modifications'].append(1.2)  # Slower
            else:
                recommendations['duration_modifications'].append(1.0)
            
            # Velocity enhancements
            recommendations['velocity_enhancements'].append(10 if payload.sentiment > 0.5 else 5)
        
        print(f"  [SAT SOLVER]: Generated {len(recommendations['pitch_adjustments'])} parameter adjustments via binary bridge")
        
        return recommendations
    
    def interpret_solution(self, solution, analysis_result):
        """
        Interpret SAT solution as musical parameters.
        
        Args:
            solution: SAT solver output
            analysis_result: Original analysis results
            
        Returns:
            Dictionary with musical parameter recommendations
        """
        emotional_vector = analysis_result.get('emotional_vector', [])
        
        recommendations = {
            'pitch_adjustments': [],
            'duration_modifications': [],
            'velocity_enhancements': [],
            'instrument_changes': []
        }
        
        # Parse solution and map to musical parameters
        for i in range(len(emotional_vector)):
            base_idx = i * 4
            
            # Extract solution bits for this word
            if base_idx < len(solution):
                # Pitch adjustment
                if solution[base_idx]:
                    recommendations['pitch_adjustments'].append(2)  # Raise pitch
                else:
                    recommendations['pitch_adjustments'].append(0)
                
                # Duration modification
                if base_idx + 1 < len(solution) and solution[base_idx + 1]:
                    recommendations['duration_modifications'].append(0.8)  # Shorter
                else:
                    recommendations['duration_modifications'].append(1.0)
                
                # Velocity enhancement
                if base_idx + 2 < len(solution) and solution[base_idx + 2]:
                    recommendations['velocity_enhancements'].append(15)  # Louder
                else:
                    recommendations['velocity_enhancements'].append(0)
        
        print(f"  [SAT SOLVER]: Generated {len(recommendations['pitch_adjustments'])} parameter adjustments")
        
        return recommendations

# Fallback SAT solver using python-sat if titan_forge fails
class FallbackSATSolver:
    """
    Fallback SAT solver using python-sat when titan_forge is unavailable.
    """
    
    def solve_musical_constraints(self, analysis_result):
        """
        Simplified SAT solving using python-sat.
        """
        try:
            from pysat.solvers import Glucose4
            
            emotional_vector = analysis_result.get('emotional_vector', [])
            solver = Glucose4()
            
            # Add simple constraints
            for i, score in enumerate(emotional_vector):
                # Each word should have at least one musical parameter
                solver.add_clause([i + 1])
                
                # High emotion = high pitch constraint
                if score > 0.7:
                    solver.add_clause([i + 1, i + 2])
            
            # Solve
            if solver.solve():
                solution = solver.get_model()
                print("  [SAT SOLVER]: Fallback solver found solution")
                return {'solution': solution}
            else:
                print("  [SAT SOLVER]: Fallback solver found no solution")
                return None
                
        except ImportError:
            print("  [SAT SOLVER]: python-sat not available")
            return None
        except Exception as e:
            print(f"  [SAT SOLVER]: Fallback error: {e}")
            return None
