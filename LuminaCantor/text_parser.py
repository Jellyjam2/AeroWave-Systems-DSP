import re
from transformers import pipeline
import numpy as np
from .sat_integration import SATMusicalSolver, FallbackSATSolver
from .cross_cultural_empathy import CrossCulturalEmpathyEngine

class AdvancedTextParser:
    """
    Advanced semantic text parser using transformer models for deep emotional understanding.
    """
    
    # Cultural musical patterns
    CULTURAL_PATTERNS = {
        'western': {
            'scales': ['major', 'minor'],
            'rhythms': [0.5, 0.75, 1.0],
            'instruments': ['piano', 'strings', 'brass']
        },
        'eastern': {
            'scales': ['pentatonic', 'blues'],
            'rhythms': [0.33, 0.66, 1.0],
            'instruments': ['koto', 'sitar', 'percussion']
        },
        'african': {
            'scales': ['pentatonic', 'blues'],
            'rhythms': [0.25, 0.5, 0.75],
            'instruments': ['drums', 'percussion', 'vocals']
        },
        'latin': {
            'scales': ['major', 'minor'],
            'rhythms': [0.5, 0.5, 0.75],
            'instruments': ['guitar', 'percussion', 'brass']
        }
    }
    
    # Contextual keywords for cultural detection
    CULTURAL_KEYWORDS = {
        'western': ['church', 'god', 'lord', 'prayer', 'hymn', 'bible', 'christian', 'european', 'western'],
        'eastern': ['zen', 'buddha', 'temple', 'meditation', 'lotus', 'cherry', 'asia', 'eastern', 'dao'],
        'african': ['drum', 'tribe', 'ancestors', 'rhythm', 'dance', 'africa', 'safari', 'jungle'],
        'latin': ['fiesta', 'amor', 'corazón', 'baile', 'música', 'latin', 'spanish', 'passion']
    }
    
    def __init__(self):
        try:
            # Initialize sentiment analysis pipeline
            self.sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
            self.use_transformers = True
            print("  [PARSER]: Advanced NLP models loaded successfully")
        except Exception as e:
            print(f"  [PARSER]: Transformer models not available, using fallback: {e}")
            self.use_transformers = False
        
        # Initialize SAT solver
        try:
            self.sat_solver = SATMusicalSolver()
            print("  [PARSER]: SAT solver (titan_forge) initialized")
        except Exception as e:
            print(f"  [PARSER]: SAT solver not available, using fallback: {e}")
            self.sat_solver = FallbackSATSolver()
        
        # Initialize cross-cultural empathy engine
        self.empathy_engine = CrossCulturalEmpathyEngine()
        print("  [PARSER]: Cross-cultural empathy engine initialized")
    
    def parse(self, text_content: str) -> dict:
        """
        Parses the input text into a comprehensive musical feature set.
        
        Args:
            text_content: The raw string content of the text.
            
        Returns:
            A dictionary containing emotional vectors, sentiment scores, and musical parameters.
        """
        result = {
            'emotional_vector': [],
            'sentiment': 0.5,
            'arousal': 0.5,
            'valence': 0.5,
            'complexity': 0.5,
            'rhythm_pattern': [],
            'harmonic_progression': [],
            'cultural_context': 'western',
            'cultural_influence': 0.0
        }
        
        # Normalize text
        processed_text = re.sub(r'[^\w\s]', '', text_content).lower()
        sentences = processed_text.split('.')
        
        # Detect cultural context
        cultural_context = self._detect_cultural_context(processed_text)
        result['cultural_context'] = cultural_context
        result['cultural_influence'] = self._calculate_cultural_influence(processed_text, cultural_context)
        
        # Analyze sentiment if transformers available
        if self.use_transformers:
            try:
                sentiment_result = self.sentiment_analyzer(text_content[:512])[0]  # Limit to 512 tokens
                result['sentiment'] = (sentiment_result['score'] if sentiment_result['label'] == 'POSITIVE' else 1 - sentiment_result['score'])
            except:
                result['sentiment'] = 0.5
        
        # Get cultural patterns
        cultural_patterns = self.CULTURAL_PATTERNS.get(cultural_context, self.CULTURAL_PATTERNS['western'])
        
        # Analyze each sentence for musical features
        for sentence in sentences:
            if not sentence.strip():
                continue
                
            words = sentence.split()
            sentence_length = len(words)
            
            for i, word in enumerate(words):
                # Multi-dimensional feature extraction with cultural influence
                features = self._extract_word_features(word, i, sentence_length, result['sentiment'], cultural_patterns)
                result['emotional_vector'].append(features['combined'])
                result['rhythm_pattern'].append(features['rhythm'])
                
                # Generate harmonic progression based on sentence structure
                if i % 3 == 0:  # Every 3rd word contributes to harmony
                    result['harmonic_progression'].append(features['harmonic'])
        
        # Calculate overall musical parameters
        result['arousal'] = np.mean([f for f in result['emotional_vector']]) if result['emotional_vector'] else 0.5
        result['valence'] = result['sentiment']
        result['complexity'] = min(len(set(processed_text.split())) / max(len(processed_text.split()), 1), 1.0)
        
        # Apply SAT solving for optimal musical patterns
        sat_solution = self.sat_solver.solve_musical_constraints(result)
        if sat_solution:
            result['sat_recommendations'] = sat_solution
            print(f"  [PARSER]: SAT solver provided musical pattern optimizations")
        else:
            result['sat_recommendations'] = None
        
        # Apply cross-cultural empathy analysis
        cultural_profile = self.empathy_engine.analyze_cultural_emotional_profile(result)
        result['cultural_profile'] = cultural_profile
        print(f"  [PARSER]: Cultural emotional profile analyzed")
        
        print(f"  [PARSER]: Generated advanced analysis with {len(result['emotional_vector'])} data points")
        print(f"  [PARSER]: Sentiment: {result['sentiment']:.2f}, Arousal: {result['arousal']:.2f}, Complexity: {result['complexity']:.2f}")
        print(f"  [PARSER]: Cultural Context: {cultural_context} (influence: {result['cultural_influence']:.2f})")
        
        return result
    
    def _detect_cultural_context(self, text: str) -> str:
        """Detect cultural context based on keyword analysis."""
        cultural_scores = {}
        
        for culture, keywords in self.CULTURAL_KEYWORDS.items():
            score = sum(1 for keyword in keywords if keyword in text.lower())
            cultural_scores[culture] = score
        
        # Return culture with highest score, default to western
        if cultural_scores:
            return max(cultural_scores, key=cultural_scores.get)
        return 'western'
    
    def _calculate_cultural_influence(self, text: str, culture: str) -> float:
        """Calculate how strongly the cultural context is present."""
        keywords = self.CULTURAL_KEYWORDS.get(culture, [])
        keyword_count = sum(1 for keyword in keywords if keyword in text.lower())
        total_words = len(text.split())
        
        return min(keyword_count / max(total_words, 1), 1.0)
    
    def _extract_word_features(self, word: str, position: int, sentence_length: int, global_sentiment: float, cultural_patterns: dict) -> dict:
        """Extract multi-dimensional musical features from a single word."""
        
        # Structural features
        length_score = min(len(word) / 10.0, 1.0)
        vowels = re.findall(r'[aeiouy]+', word.lower())
        syllable_score = min(len(vowels) / 4.0, 1.0)
        vowel_density = sum(1 for char in word if char in 'aeiou') / max(len(word), 1)
        
        # Position-based emphasis
        if position == 0 or position == sentence_length - 1:
            position_score = 1.0
        elif position < sentence_length * 0.3 or position > sentence_length * 0.7:
            position_score = 0.8
        else:
            position_score = 0.6
        
        # Semantic influence (if transformers available)
        semantic_weight = global_sentiment if self.use_transformers else 0.5
        
        # Cultural rhythm influence
        cultural_rhythm = cultural_patterns.get('rhythms', [0.5])[position % len(cultural_patterns.get('rhythms', [0.5]))]
        
        # Combined emotional score with cultural influence
        combined = (
            (length_score * 0.20) +
            (syllable_score * 0.15) +
            (vowel_density * 0.15) +
            (position_score * 0.15) +
            (semantic_weight * 0.20) +
            (cultural_rhythm * 0.15)
        )
        
        # Rhythm pattern (based on syllable complexity and cultural patterns)
        rhythm = 0.5 + (syllable_score * 0.25) + (cultural_rhythm * 0.25)
        
        # Harmonic potential (based on word complexity and position)
        harmonic = (length_score + position_score) / 2
        
        return {
            'combined': combined,
            'rhythm': rhythm,
            'harmonic': harmonic
        }

# Maintain backward compatibility
def parse(text_content: str) -> list[float]:
    """Legacy function for backward compatibility."""
    parser = AdvancedTextParser()
    result = parser.parse(text_content)
    return result['emotional_vector']

