"""
Memory Monitoring Hook using Python's tracemalloc
Verifies that ZeroAllocationAudioStream operates with completely flat memory graph (0 bytes of new heap allocation)
"""

import tracemalloc
import time
import sys
import os
from typing import Dict, Any, List
from collections import defaultdict

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from LuminaCantor.zero_allocation_stream import ZeroAllocationAudioStream, FixedSizeMemoryWindow

class MemoryMonitor:
    """
    Memory monitoring system for zero-allocation verification.
    Uses tracemalloc to track heap allocations during audio streaming.
    """
    
    def __init__(self):
        """Initialize memory monitor."""
        print("  [MEMORY MONITOR]: Initializing memory tracking system...")
        tracemalloc.start()
        self.baseline = None
        self.snapshots = []
        self.allocation_counts = defaultdict(int)
    
    def capture_baseline(self):
        """Capture baseline memory usage."""
        self.baseline = tracemalloc.take_snapshot()
        print(f"  [MEMORY MONITOR]: Baseline captured - {self._format_size(self._get_total_size(self.baseline))}")
    
    def capture_snapshot(self, label: str = ""):
        """
        Capture memory snapshot.
        
        Args:
            label: Label for the snapshot
        """
        snapshot = tracemalloc.take_snapshot()
        self.snapshots.append((label, snapshot, time.time()))
        print(f"  [MEMORY MONITOR]: Snapshot '{label}' - {self._format_size(self._get_total_size(snapshot))}")
    
    def _get_total_size(self, snapshot) -> int:
        """Get total memory size from snapshot."""
        return sum(stat.size for stat in snapshot.statistics('lineno'))
    
    def _format_size(self, size_bytes: int) -> str:
        """Format size in human-readable format."""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.2f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.2f} MB"
    
    def compare_snapshots(self, snapshot1, snapshot2, label: str = "") -> Dict[str, Any]:
        """
        Compare two memory snapshots.
        
        Args:
            snapshot1: First snapshot
            snapshot2: Second snapshot
            label: Label for comparison
            
        Returns:
            Comparison results
        """
        stats = snapshot2.compare_to(snapshot1, 'lineno')
        
        total_allocated = sum(stat.size_diff for stat in stats if stat.size_diff > 0)
        total_freed = sum(abs(stat.size_diff) for stat in stats if stat.size_diff < 0)
        net_change = self._get_total_size(snapshot2) - self._get_total_size(snapshot1)
        
        return {
            'label': label,
            'total_allocated': total_allocated,
            'total_freed': total_freed,
            'net_change': net_change,
            'allocation_count': len([s for s in stats if s.size_diff > 0]),
            'free_count': len([s for s in stats if s.size_diff < 0]),
            'top_allocations': stats[:5] if stats else []
        }
    
    def verify_zero_allocation(self, operation_func, *args, **kwargs) -> Dict[str, Any]:
        """
        Verify that an operation performs zero heap allocations.
        
        Args:
            operation_func: Function to test
            *args: Function arguments
            **kwargs: Function keyword arguments
            
        Returns:
            Verification results
        """
        print(f"  [MEMORY MONITOR]: Verifying zero-allocation for {operation_func.__name__}...")
        
        # Capture before snapshot
        before = tracemalloc.take_snapshot()
        
        # Execute operation
        result = operation_func(*args, **kwargs)
        
        # Capture after snapshot
        after = tracemalloc.take_snapshot()
        
        # Compare
        comparison = self.compare_snapshots(before, after, operation_func.__name__)
        
        # Determine if zero-allocation
        is_zero_allocation = comparison['total_allocated'] == 0
        
        print(f"  [MEMORY MONITOR]: Allocated: {self._format_size(comparison['total_allocated'])}")
        print(f"  [MEMORY MONITOR]: Freed: {self._format_size(comparison['total_freed'])}")
        print(f"  [MEMORY MONITOR]: Net change: {self._format_size(comparison['net_change'])}")
        print(f"  [MEMORY MONITOR]: Zero-allocation: {is_zero_allocation}")
        
        return {
            'is_zero_allocation': is_zero_allocation,
            'comparison': comparison,
            'result': result
        }
    
    def print_allocation_report(self):
        """Print detailed allocation report."""
        print("\n" + "=" * 70)
        print("  [MEMORY MONITOR]: DETAILED ALLOCATION REPORT")
        print("=" * 70)
        
        if not self.snapshots:
            print("  [MEMORY MONITOR]: No snapshots captured")
            return
        
        # Print timeline
        print("\n  [MEMORY TIMELINE]")
        for i, (label, snapshot, timestamp) in enumerate(self.snapshots):
            size = self._get_total_size(snapshot)
            print(f"    {i+1}. {label}: {self._format_size(size)}")
        
        # Compare consecutive snapshots
        print("\n  [ALLOCATION CHANGES]")
        for i in range(1, len(self.snapshots)):
            label1, snapshot1, _ = self.snapshots[i-1]
            label2, snapshot2, _ = self.snapshots[i]
            
            comparison = self.compare_snapshots(snapshot1, snapshot2, f"{label1} -> {label2}")
            
            print(f"\n    {label1} → {label2}:")
            print(f"      Allocated: {self._format_size(comparison['total_allocated'])}")
            print(f"      Freed: {self._format_size(comparison['total_freed'])}")
            print(f"      Net change: {self._format_size(comparison['net_change'])}")
            print(f"      Allocation count: {comparison['allocation_count']}")
            
            if comparison['top_allocations']:
                print(f"      Top allocations:")
                for stat in comparison['top_allocations']:
                    print(f"        {stat.traceback.format()[-1]}: {self._format_size(stat.size_diff)}")
    
    def stop(self):
        """Stop memory monitoring."""
        tracemalloc.stop()
        print("  [MEMORY MONITOR]: Memory tracking stopped")


class ZeroAllocationVerifier:
    """
    Specific verifier for zero-allocation audio streaming.
    """
    
    def __init__(self):
        """Initialize verifier."""
        self.monitor = MemoryMonitor()
        self.audio_stream = ZeroAllocationAudioStream()
    
    def test_fixed_size_window(self) -> Dict[str, Any]:
        """Test fixed-size memory window for zero allocations."""
        print("\n  [VERIFIER]: Testing FixedSizeMemoryWindow...")
        
        def write_operation():
            window = FixedSizeMemoryWindow()
            test_data = b'\x00' * 100
            return window.write_bytes(test_data)
        
        def read_operation():
            window = FixedSizeMemoryWindow()
            test_data = b'\x00' * 100
            window.write_bytes(test_data)
            return window.read_bytes(50)
        
        write_result = self.monitor.verify_zero_allocation(write_operation)
        read_result = self.monitor.verify_zero_allocation(read_operation)
        
        return {
            'write_zero_allocation': write_result['is_zero_allocation'],
            'read_zero_allocation': read_result['is_zero_allocation'],
            'write_allocated': write_result['comparison']['total_allocated'],
            'read_allocated': read_result['comparison']['total_allocated']
        }
    
    def test_audio_stream(self) -> Dict[str, Any]:
        """Test audio stream for zero allocations."""
        print("\n  [VERIFIER]: Testing ZeroAllocationAudioStream...")
        
        def stream_operation():
            test_audio = b'\x00' * 100
            return self.audio_stream.write_audio_chunk(test_audio)
        
        result = self.monitor.verify_zero_allocation(stream_operation)
        
        return {
            'stream_zero_allocation': result['is_zero_allocation'],
            'allocated': result['comparison']['total_allocated']
        }
    
    def test_continuous_streaming(self, iterations: int = 100) -> Dict[str, Any]:
        """
        Test continuous streaming for memory stability.
        
        Args:
            iterations: Number of streaming iterations
            
        Returns:
            Test results
        """
        print(f"\n  [VERIFIER]: Testing continuous streaming ({iterations} iterations)...")
        
        self.monitor.capture_baseline()
        
        audio_data = b'\x00' * 512
        allocations_per_iteration = []
        
        for i in range(iterations):
            before = tracemalloc.take_snapshot()
            
            self.audio_stream.write_audio_chunk(audio_data)
            self.audio_stream.read_audio_chunk(256)
            
            after = tracemalloc.take_snapshot()
            comparison = self.monitor.compare_snapshots(before, after, f"iteration_{i}")
            allocations_per_iteration.append(comparison['total_allocated'])
        
        self.monitor.capture_snapshot("continuous_streaming_complete")
        
        avg_allocation = sum(allocations_per_iteration) / len(allocations_per_iteration)
        max_allocation = max(allocations_per_iteration)
        zero_alloc_count = sum(1 for a in allocations_per_iteration if a == 0)
        
        return {
            'iterations': iterations,
            'avg_allocation_per_iteration': avg_allocation,
            'max_allocation': max_allocation,
            'zero_allocation_count': zero_alloc_count,
            'zero_allocation_rate': zero_alloc_count / iterations,
            'is_stable': avg_allocation == 0
        }
    
    def run_comprehensive_verification(self) -> Dict[str, Any]:
        """Run comprehensive zero-allocation verification."""
        print("\n" + "=" * 70)
        print("  ZERO-ALLOCATION VERIFICATION SUITE")
        print("=" * 70)
        
        self.monitor.capture_baseline()
        
        # Test fixed-size window
        window_results = self.test_fixed_size_window()
        
        # Test audio stream
        stream_results = self.test_audio_stream()
        
        # Test continuous streaming
        continuous_results = self.test_continuous_streaming(iterations=50)
        
        # Print report
        self.monitor.print_allocation_report()
        
        # Summary
        print("\n" + "=" * 70)
        print("  [VERIFICATION SUMMARY]")
        print("=" * 70)
        print(f"  FixedSizeMemoryWindow write: {window_results['write_zero_allocation']}")
        print(f"  FixedSizeMemoryWindow read: {window_results['read_zero_allocation']}")
        print(f"  AudioStream: {stream_results['stream_zero_allocation']}")
        print(f"  Continuous streaming stability: {continuous_results['is_stable']}")
        print(f"  Zero-allocation rate: {continuous_results['zero_allocation_rate']*100:.1f}%")
        
        overall_success = (
            window_results['write_zero_allocation'] and
            window_results['read_zero_allocation'] and
            stream_results['stream_zero_allocation'] and
            continuous_results['is_stable']
        )
        
        print(f"\n  Overall zero-allocation: {overall_success}")
        print("=" * 70)
        
        return {
            'window_results': window_results,
            'stream_results': stream_results,
            'continuous_results': continuous_results,
            'overall_success': overall_success
        }
    
    def cleanup(self):
        """Cleanup resources."""
        self.monitor.stop()


def main():
    """Main verification execution."""
    print("\n" + "=" * 70)
    print("  ZERO-ALLOCATION AUDIO STREAMING VERIFICATION")
    print("=" * 70 + "\n")
    
    verifier = ZeroAllocationVerifier()
    results = verifier.run_comprehensive_verification()
    verifier.cleanup()
    
    print("\n  [VERIFIER]: Verification complete")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
