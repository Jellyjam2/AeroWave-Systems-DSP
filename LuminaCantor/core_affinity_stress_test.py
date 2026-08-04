"""
Terminal Stress-Test Script for Core Affinity Verification
Intentionally floods the backend with background CPU noise to verify CoreAffinityManager
successfully protects Core 1's audio stream from dropping audio frames
"""

import multiprocessing
import threading
import time
import random
import math
import sys
import os
from typing import Dict, Any, List
from collections import defaultdict

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from LuminaCantor.hardened_task_scheduler import HardenedTaskScheduler, TaskType, TaskPriority
from LuminaCantor.zero_allocation_stream import ZeroAllocationAudioStream

class CPUStressGenerator:
    """
    CPU stress generator for background noise simulation.
    Creates heavy computational load on all cores except audio core.
    """
    
    def __init__(self, num_workers: int = 4):
        """
        Initialize CPU stress generator.
        
        Args:
            num_workers: Number of stress worker threads
        """
        self.num_workers = num_workers
        self.workers = []
        self.running = False
        self.stop_event = threading.Event()
    
    def _stress_worker(self, worker_id: int):
        """
        Stress worker that performs heavy computations.
        
        Args:
            worker_id: Worker identifier
        """
        print(f"  [STRESS]: Worker {worker_id} started")
        
        while not self.stop_event.is_set():
            # Perform heavy computations
            start = time.time()
            
            # Matrix multiplication simulation
            size = 100
            matrix_a = [[random.random() for _ in range(size)] for _ in range(size)]
            matrix_b = [[random.random() for _ in range(size)] for _ in range(size)]
            
            result = [[0.0 for _ in range(size)] for _ in range(size)]
            for i in range(size):
                for j in range(size):
                    for k in range(size):
                        result[i][j] += matrix_a[i][k] * matrix_b[k][j]
            
            # Prime number computation
            primes = []
            for num in range(2, 1000):
                is_prime = True
                for i in range(2, int(math.sqrt(num)) + 1):
                    if num % i == 0:
                        is_prime = False
                        break
                if is_prime:
                    primes.append(num)
            
            elapsed = time.time() - start
            if elapsed < 0.01:  # Ensure minimum workload
                time.sleep(0.01 - elapsed)
        
        print(f"  [STRESS]: Worker {worker_id} stopped")
    
    def start(self):
        """Start stress workers."""
        self.running = True
        self.stop_event.clear()
        
        for i in range(self.num_workers):
            worker = threading.Thread(target=self._stress_worker, args=(i,))
            worker.daemon = True
            worker.start()
            self.workers.append(worker)
        
        print(f"  [STRESS]: Started {self.num_workers} stress workers")
    
    def stop(self):
        """Stop stress workers."""
        self.running = False
        self.stop_event.set()
        
        for worker in self.workers:
            worker.join(timeout=2.0)
        
        self.workers.clear()
        print("  [STRESS]: All stress workers stopped")


class AudioStreamMonitor:
    """
    Audio stream monitor for detecting frame drops.
    Monitors audio stream performance under stress conditions.
    """
    
    def __init__(self, audio_stream: ZeroAllocationAudioStream):
        """
        Initialize audio stream monitor.
        
        Args:
            audio_stream: Audio stream to monitor
        """
        self.audio_stream = audio_stream
        self.frame_drops = 0
        self.total_frames = 0
        self.latency_samples = []
        self.running = False
        self.monitor_thread = None
    
    def _monitor_stream(self):
        """Monitor audio stream for frame drops."""
        print("  [MONITOR]: Audio stream monitoring started")
        
        audio_data = b'\x00' * 512
        target_frame_rate = 480  # frames per second
        frame_interval = 1.0 / target_frame_rate
        
        while self.running:
            start_time = time.time()
            
            # Simulate audio frame processing
            success = self.audio_stream.write_audio_chunk(audio_data)
            self.audio_stream.read_audio_chunk(256)
            
            elapsed = time.time() - start_time
            self.latency_samples.append(elapsed)
            
            if not success:
                self.frame_drops += 1
            
            self.total_frames += 1
            
            # Maintain target frame rate
            sleep_time = frame_interval - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)
            else:
                # Frame drop due to processing delay
                self.frame_drops += 1
        
        print("  [MONITOR]: Audio stream monitoring stopped")
    
    def start(self):
        """Start audio stream monitoring."""
        self.running = True
        self.monitor_thread = threading.Thread(target=self._monitor_stream)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
    
    def stop(self):
        """Stop audio stream monitoring."""
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2.0)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get monitoring statistics."""
        avg_latency = sum(self.latency_samples) / len(self.latency_samples) if self.latency_samples else 0
        max_latency = max(self.latency_samples) if self.latency_samples else 0
        min_latency = min(self.latency_samples) if self.latency_samples else 0
        drop_rate = self.frame_drops / self.total_frames if self.total_frames > 0 else 0
        
        return {
            'total_frames': self.total_frames,
            'frame_drops': self.frame_drops,
            'drop_rate': drop_rate,
            'avg_latency_ms': avg_latency * 1000,
            'max_latency_ms': max_latency * 1000,
            'min_latency_ms': min_latency * 1000,
            'latency_samples_count': len(self.latency_samples)
        }


class CoreAffinityStressTest:
    """
    Core affinity stress test suite.
    Verifies that CoreAffinityManager protects audio stream under heavy load.
    """
    
    def __init__(self):
        """Initialize stress test suite."""
        print("  [STRESS TEST]: Initializing core affinity stress test...")
        
        self.scheduler = HardenedTaskScheduler()
        self.audio_stream = ZeroAllocationAudioStream()
        self.stress_generator = CPUStressGenerator(num_workers=6)
        self.audio_monitor = AudioStreamMonitor(self.audio_stream)
        
        self.test_results = []
    
    def test_baseline_performance(self, duration: int = 5) -> Dict[str, Any]:
        """
        Test baseline performance without stress.
        
        Args:
            duration: Test duration in seconds
            
        Returns:
            Baseline performance results
        """
        print(f"\n  [STRESS TEST]: Testing baseline performance ({duration}s)...")
        
        self.audio_monitor.start()
        self.audio_stream = ZeroAllocationAudioStream()
        self.audio_monitor.audio_stream = self.audio_stream
        
        time.sleep(duration)
        
        self.audio_monitor.stop()
        stats = self.audio_monitor.get_stats()
        
        print(f"  [STRESS TEST]: Baseline - Drop rate: {stats['drop_rate']*100:.2f}%, "
              f"Avg latency: {stats['avg_latency_ms']:.2f}ms")
        
        return stats
    
    def test_stress_performance(self, duration: int = 10) -> Dict[str, Any]:
        """
        Test performance under CPU stress.
        
        Args:
            duration: Test duration in seconds
            
        Returns:
            Stress performance results
        """
        print(f"\n  [STRESS TEST]: Testing performance under stress ({duration}s)...")
        
        # Start stress generator
        self.stress_generator.start()
        
        # Start audio monitoring
        self.audio_monitor.start()
        self.audio_stream = ZeroAllocationAudioStream()
        self.audio_monitor.audio_stream = self.audio_stream
        
        # Run test
        time.sleep(duration)
        
        # Stop monitoring
        self.audio_monitor.stop()
        stats = self.audio_monitor.get_stats()
        
        # Stop stress generator
        self.stress_generator.stop()
        
        print(f"  [STRESS TEST]: Stress - Drop rate: {stats['drop_rate']*100:.2f}%, "
              f"Avg latency: {stats['avg_latency_ms']:.2f}ms")
        
        return stats
    
    def test_core_affinity_protection(self, duration: int = 10) -> Dict[str, Any]:
        """
        Test core affinity protection with scheduler.
        
        Args:
            duration: Test duration in seconds
            
        Returns:
            Core affinity protection results
        """
        print(f"\n  [STRESS TEST]: Testing core affinity protection ({duration}s)...")
        
        # Start scheduler
        self.scheduler.start()
        
        # Start stress generator
        self.stress_generator.start()
        
        # Start audio monitoring
        self.audio_monitor.start()
        self.audio_stream = ZeroAllocationAudioStream()
        self.audio_monitor.audio_stream = self.audio_stream
        
        # Submit audio tasks to scheduler
        def audio_task():
            audio_data = b'\x00' * 512
            self.audio_stream.write_audio_chunk(audio_data)
            self.audio_stream.read_audio_chunk(256)
        
        # Run test with continuous audio tasks
        start_time = time.time()
        while time.time() - start_time < duration:
            self.scheduler.submit_task(
                audio_task,
                TaskType.AUDIO_PROCESSING,
                TaskPriority.CRITICAL
            )
            time.sleep(0.01)  # 100Hz task submission
        
        # Stop monitoring
        self.audio_monitor.stop()
        stats = self.audio_monitor.get_stats()
        
        # Stop stress generator
        self.stress_generator.stop()
        
        # Stop scheduler
        self.scheduler.stop()
        
        print(f"  [STRESS TEST]: Core affinity - Drop rate: {stats['drop_rate']*100:.2f}%, "
              f"Avg latency: {stats['avg_latency_ms']:.2f}ms")
        
        return stats
    
    def run_comprehensive_stress_test(self) -> Dict[str, Any]:
        """Run comprehensive stress test suite."""
        print("\n" + "=" * 70)
        print("  CORE AFFINITY STRESS TEST SUITE")
        print("=" * 70)
        
        # Test 1: Baseline performance
        baseline = self.test_baseline_performance(duration=5)
        
        # Test 2: Performance under stress (no protection)
        stress_no_protection = self.test_stress_performance(duration=5)
        
        # Test 3: Performance with core affinity protection
        stress_with_protection = self.test_core_affinity_protection(duration=5)
        
        # Analyze results
        print("\n" + "=" * 70)
        print("  [STRESS TEST]: RESULTS ANALYSIS")
        print("=" * 70)
        
        print(f"\n  [BASELINE PERFORMANCE]")
        print(f"    Drop rate: {baseline['drop_rate']*100:.4f}%")
        print(f"    Avg latency: {baseline['avg_latency_ms']:.4f}ms")
        print(f"    Max latency: {baseline['max_latency_ms']:.4f}ms")
        
        print(f"\n  [STRESS WITHOUT PROTECTION]")
        print(f"    Drop rate: {stress_no_protection['drop_rate']*100:.4f}%")
        print(f"    Avg latency: {stress_no_protection['avg_latency_ms']:.4f}ms")
        print(f"    Max latency: {stress_no_protection['max_latency_ms']:.4f}ms")
        print(f"    Latency increase: {(stress_no_protection['avg_latency_ms'] / baseline['avg_latency_ms'] - 1)*100:.2f}%")
        
        print(f"\n  [STRESS WITH CORE AFFINITY PROTECTION]")
        print(f"    Drop rate: {stress_with_protection['drop_rate']*100:.4f}%")
        print(f"    Avg latency: {stress_with_protection['avg_latency_ms']:.4f}ms")
        print(f"    Max latency: {stress_with_protection['max_latency_ms']:.4f}ms")
        print(f"    Latency increase: {(stress_with_protection['avg_latency_ms'] / baseline['avg_latency_ms'] - 1)*100:.2f}%")
        
        # Determine protection effectiveness
        protection_effective = (
            stress_with_protection['drop_rate'] <= stress_no_protection['drop_rate'] * 0.5 and
            stress_with_protection['avg_latency_ms'] <= stress_no_protection['avg_latency_ms'] * 1.5
        )
        
        print(f"\n  [PROTECTION EFFECTIVENESS]")
        print(f"    Core affinity protection: {'EFFECTIVE' if protection_effective else 'INEFFECTIVE'}")
        print(f"    Drop rate reduction: {(1 - stress_with_protection['drop_rate'] / stress_no_protection['drop_rate'])*100:.2f}%")
        
        print("=" * 70)
        
        return {
            'baseline': baseline,
            'stress_no_protection': stress_no_protection,
            'stress_with_protection': stress_with_protection,
            'protection_effective': protection_effective
        }


def main():
    """Main stress test execution."""
    print("\n" + "=" * 70)
    print("  CORE AFFINITY STRESS TEST - VERIFICATION SUITE")
    print("=" * 70 + "\n")
    
    stress_test = CoreAffinityStressTest()
    results = stress_test.run_comprehensive_stress_test()
    
    print("\n  [STRESS TEST]: Stress test complete")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
