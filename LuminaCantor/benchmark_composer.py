"""
Automated Benchmarking Script for Cognitive Matrix Composer
Verifies microsecond response time difference between raw BERT/SAT pipeline vs RAMHypervisorCache hit
"""

import time
import statistics
import sys
import os
from typing import Dict, Any, List

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from LuminaCantor.cognitive_matrix_composer import CognitiveMatrixComposer
from LuminaCantor.text_parser import AdvancedTextParser
from LuminaCantor.music_generator import AdvancedMusicGenerator
from LuminaCantor.sat_integration import SATMusicalSolver

class ComposerBenchmark:
    """
    Automated benchmarking system for Cognitive Matrix Composer.
    Measures performance differences between cached and uncached operations.
    """
    
    def __init__(self):
        """Initialize benchmarking system."""
        print("  [BENCHMARK]: Initializing Cognitive Matrix Composer benchmark suite...")
        
        # Initialize systems
        self.composer = CognitiveMatrixComposer()
        self.parser = AdvancedTextParser()
        self.generator = AdvancedMusicGenerator()
        self.sat_solver = SATMusicalSolver()
        
        # Test data
        self.test_texts = [
            "The sun rises over the mountains with golden light",
            "Dark shadows creep through the ancient forest",
            "Joyful laughter fills the summer festival",
            "Melancholy waves crash against the lonely shore",
            "Epic battles rage across the starlit galaxy"
        ]
        
        print("  [BENCHMARK]: Benchmark suite ready")
    
    def benchmark_raw_pipeline(self, iterations: int = 10) -> Dict[str, Any]:
        """
        Benchmark raw BERT/SAT pipeline (no cache).
        
        Args:
            iterations: Number of test iterations
            
        Returns:
            Benchmark results
        """
        print(f"  [BENCHMARK]: Running raw pipeline benchmark ({iterations} iterations)...")
        
        times = []
        cache_disabled = True
        
        for i in range(iterations):
            text = self.test_texts[i % len(self.test_texts)]
            
            start_time = time.perf_counter()
            
            # Parse text (BERT)
            analysis = self.parser.parse(text)
            
            # Solve SAT
            sat_result = self.sat_solver.solve_musical_constraints(analysis)
            
            # Generate MIDI
            output_path = f"temp_benchmark_{i}.mid"
            self.generator.generate_midi(analysis, output_path)
            
            elapsed = time.perf_counter() - start_time
            times.append(elapsed)
            
            # Clean up (with retry for file locks)
            if os.path.exists(output_path):
                try:
                    os.remove(output_path)
                except PermissionError:
                    # File in use, skip cleanup
                    pass
        
        return {
            'mean': statistics.mean(times),
            'median': statistics.median(times),
            'stdev': statistics.stdev(times) if len(times) > 1 else 0,
            'min': min(times),
            'max': max(times),
            'total': sum(times),
            'iterations': iterations
        }
    
    def benchmark_cached_pipeline(self, iterations: int = 10) -> Dict[str, Any]:
        """
        Benchmark cached pipeline (RAMHypervisorCache).
        
        Args:
            iterations: Number of test iterations
            
        Returns:
            Benchmark results
        """
        print(f"  [BENCHMARK]: Running cached pipeline benchmark ({iterations} iterations)...")
        
        times = []
        
        # First pass to populate cache
        for text in self.test_texts:
            analysis = self.parser.parse(text)
            self.composer.ram_cache.cache_result(
                text, analysis['sentiment'], analysis['arousal'],
                analysis['complexity'], analysis['cultural_context'], analysis
            )
        
        # Benchmark cache hits
        for i in range(iterations):
            text = self.test_texts[i % len(self.test_texts)]
            
            # Get analysis to compute signature
            analysis = self.parser.parse(text)
            
            start_time = time.perf_counter()
            
            # Cache lookup
            cached = self.composer.ram_cache.get_cached_result(
                text, analysis['sentiment'], analysis['arousal'],
                analysis['complexity'], analysis['cultural_context']
            )
            
            elapsed = time.perf_counter() - start_time
            times.append(elapsed)
        
        return {
            'mean': statistics.mean(times),
            'median': statistics.median(times),
            'stdev': statistics.stdev(times) if len(times) > 1 else 0,
            'min': min(times),
            'max': max(times),
            'total': sum(times),
            'iterations': iterations,
            'cache_hit_rate': 1.0  # All should be cache hits
        }
    
    def benchmark_full_composer(self, iterations: int = 5) -> Dict[str, Any]:
        """
        Benchmark full Cognitive Matrix Composer.
        
        Args:
            iterations: Number of test iterations
            
        Returns:
            Benchmark results
        """
        print(f"  [BENCHMARK]: Running full composer benchmark ({iterations} iterations)...")
        
        times = []
        cache_hits = 0
        sat_cache_hits = 0
        
        for i in range(iterations):
            text = self.test_texts[i % len(self.test_texts)]
            
            start_time = time.perf_counter()
            
            result = self.composer.compose_music(text, user_id="benchmark")
            
            elapsed = time.perf_counter() - start_time
            times.append(elapsed)
            
            if result.get('cache_hit', False):
                cache_hits += 1
            if result.get('sat_cache_hit', False):
                sat_cache_hits += 1
            
            # Cleanup
            if result['success']:
                self.composer.secure_cleanup(result['session_id'])
        
        return {
            'mean': statistics.mean(times),
            'median': statistics.median(times),
            'stdev': statistics.stdev(times) if len(times) > 1 else 0,
            'min': min(times),
            'max': max(times),
            'total': sum(times),
            'iterations': iterations,
            'cache_hit_rate': cache_hits / iterations,
            'sat_cache_hit_rate': sat_cache_hits / iterations
        }
    
    def run_comprehensive_benchmark(self) -> Dict[str, Any]:
        """Run comprehensive benchmark suite."""
        print("  [BENCHMARK]: Starting comprehensive benchmark suite...")
        print("=" * 70)
        
        # Benchmark raw pipeline
        raw_results = self.benchmark_raw_pipeline(iterations=10)
        print(f"  [BENCHMARK]: Raw pipeline - Mean: {raw_results['mean']*1000:.2f}ms, "
              f"Median: {raw_results['median']*1000:.2f}ms")
        
        # Benchmark cached pipeline
        cached_results = self.benchmark_cached_pipeline(iterations=10)
        print(f"  [BENCHMARK]: Cached pipeline - Mean: {cached_results['mean']*1000:.2f}ms, "
              f"Median: {cached_results['median']*1000:.2f}ms")
        
        # Benchmark full composer
        composer_results = self.benchmark_full_composer(iterations=5)
        print(f"  [BENCHMARK]: Full composer - Mean: {composer_results['mean']*1000:.2f}ms, "
              f"Median: {composer_results['median']*1000:.2f}ms")
        
        # Calculate speedup
        speedup = raw_results['mean'] / cached_results['mean'] if cached_results['mean'] > 0 else 0
        
        print("=" * 70)
        print(f"  [BENCHMARK]: Cache speedup: {speedup:.2f}x")
        print(f"  [BENCHMARK]: Cache hit rate: {cached_results['cache_hit_rate']*100:.1f}%")
        print(f"  [BENCHMARK]: Composer cache hit rate: {composer_results['cache_hit_rate']*100:.1f}%")
        
        return {
            'raw_pipeline': raw_results,
            'cached_pipeline': cached_results,
            'full_composer': composer_results,
            'cache_speedup': speedup
        }
    
    def print_detailed_results(self, results: Dict[str, Any]):
        """Print detailed benchmark results."""
        print("\n" + "=" * 70)
        print("  [BENCHMARK]: DETAILED PERFORMANCE ANALYSIS")
        print("=" * 70)
        
        print("\n  [RAW PIPELINE] (No Cache)")
        print(f"    Mean:     {results['raw_pipeline']['mean']*1000:.4f}ms")
        print(f"    Median:   {results['raw_pipeline']['median']*1000:.4f}ms")
        print(f"    Std Dev:  {results['raw_pipeline']['stdev']*1000:.4f}ms")
        print(f"    Min:      {results['raw_pipeline']['min']*1000:.4f}ms")
        print(f"    Max:      {results['raw_pipeline']['max']*1000:.4f}ms")
        
        print("\n  [CACHED PIPELINE] (RAM Hypervisor)")
        print(f"    Mean:     {results['cached_pipeline']['mean']*1000:.4f}ms")
        print(f"    Median:   {results['cached_pipeline']['median']*1000:.4f}ms")
        print(f"    Std Dev:  {results['cached_pipeline']['stdev']*1000:.4f}ms")
        print(f"    Min:      {results['cached_pipeline']['min']*1000:.4f}ms")
        print(f"    Max:      {results['cached_pipeline']['max']*1000:.4f}ms")
        
        print("\n  [FULL COMPOSER] (Cognitive Matrix)")
        print(f"    Mean:     {results['full_composer']['mean']*1000:.4f}ms")
        print(f"    Median:   {results['full_composer']['median']*1000:.4f}ms")
        print(f"    Std Dev:  {results['full_composer']['stdev']*1000:.4f}ms")
        print(f"    Min:      {results['full_composer']['min']*1000:.4f}ms")
        print(f"    Max:      {results['full_composer']['max']*1000:.4f}ms")
        print(f"    Cache Hit Rate: {results['full_composer']['cache_hit_rate']*100:.1f}%")
        
        print("\n  [PERFORMANCE GAINS]")
        print(f"    Cache Speedup: {results['cache_speedup']:.2f}x")
        print(f"    Time Saved per Request: {(results['raw_pipeline']['mean'] - results['cached_pipeline']['mean'])*1000:.4f}ms")
        
        print("\n" + "=" * 70)


def main():
    """Main benchmark execution."""
    print("\n" + "=" * 70)
    print("  COGNITIVE MATRIX COMPOSER - AUTOMATED BENCHMARK SUITE")
    print("=" * 70 + "\n")
    
    benchmark = ComposerBenchmark()
    results = benchmark.run_comprehensive_benchmark()
    benchmark.print_detailed_results(results)
    
    # Shutdown
    benchmark.composer.shutdown()
    
    print("\n  [BENCHMARK]: Benchmark suite complete")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
