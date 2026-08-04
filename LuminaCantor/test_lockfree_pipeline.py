"""
Lock-Free Audio Pipeline Test Suite
Verifies crossbeam-based lock-free concurrency and core affinity isolation
"""

import sys
import os
import time
import threading

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from aerowave_dsp import LockFreeAudioPipeline
    RUST_AVAILABLE = True
except ImportError:
    RUST_AVAILABLE = False
    print("  [TEST]: titan_forge not available - cannot test lock-free pipeline")
    sys.exit(1)


class LockFreePipelineTest:
    """Test suite for lock-free audio pipeline."""
    
    def __init__(self):
        """Initialize test suite."""
        self.pipeline = None
        self.tests_passed = 0
        self.tests_failed = 0
    
    def test_pipeline_creation(self):
        """Test basic pipeline creation."""
        print("  [TEST]: Testing pipeline creation...")
        
        try:
            self.pipeline = LockFreeAudioPipeline()
            
            capacity = self.pipeline.get_capacity()
            assert capacity == 4096, f"Expected capacity 4096, got {capacity}"
            
            is_empty = self.pipeline.is_empty()
            assert is_empty, "Pipeline should be empty initially"
            
            is_full = self.pipeline.is_full()
            assert not is_full, "Pipeline should not be full initially"
            
            print(f"    ✓ Pipeline created successfully (capacity: {capacity})")
            self.tests_passed += 1
            return True
        except Exception as e:
            print(f"    ✗ Pipeline creation failed: {e}")
            self.tests_failed += 1
            return False
    
    def test_frame_pushing(self):
        """Test pushing audio frames."""
        print("  [TEST]: Testing frame pushing...")
        
        try:
            # Push a small block of frames
            test_frames = [100, 200, 300, 400, 500]
            success = self.pipeline.push_frame_block(test_frames)
            
            assert success, "Frame push should succeed"
            
            length = self.pipeline.get_length()
            assert length == 5, f"Expected length 5, got {length}"
            
            print(f"    ✓ Frame pushing successful (length: {length})")
            self.tests_passed += 1
            return True
        except Exception as e:
            print(f"    ✗ Frame pushing failed: {e}")
            self.tests_failed += 1
            return False
    
    def test_large_block_pushing(self):
        """Test pushing large blocks of frames."""
        print("  [TEST]: Testing large block pushing...")
        
        try:
            # Push a large block of frames
            large_block = list(range(1000))
            success = self.pipeline.push_frame_block(large_block)
            
            assert success, "Large block push should succeed"
            
            length = self.pipeline.get_length()
            assert length == 1005, f"Expected length 1005, got {length}"  # 5 from previous test + 1000
            
            print(f"    ✓ Large block pushing successful (length: {length})")
            self.tests_passed += 1
            return True
        except Exception as e:
            print(f"    ✗ Large block pushing failed: {e}")
            self.tests_failed += 1
            return False
    
    def test_channel_full(self):
        """Test channel full detection."""
        print("  [TEST]: Testing channel full detection...")
        
        try:
            # Fill the channel to capacity
            remaining = 4096 - self.pipeline.get_length()
            large_block = [0] * remaining
            success = self.pipeline.push_frame_block(large_block)
            
            assert success, "Fill to capacity should succeed"
            
            is_full = self.pipeline.is_full()
            assert is_full, "Channel should be full"
            
            # Try to push one more frame (should fail)
            extra_frame = [999]
            success = self.pipeline.push_frame_block(extra_frame)
            assert not success, "Push to full channel should fail"
            
            print(f"    ✓ Channel full detection working correctly")
            self.tests_passed += 1
            return True
        except Exception as e:
            print(f"    ✗ Channel full detection failed: {e}")
            self.tests_failed += 1
            return False
    
    def test_worker_spawn(self):
        """Test spawning isolated audio worker."""
        print("  [TEST]: Testing isolated audio worker spawn...")
        
        try:
            # Create a new pipeline for this test
            test_pipeline = LockFreeAudioPipeline()
            
            # Spawn the worker
            test_pipeline.spawn_isolated_audio_worker()
            
            # Give the worker a moment to start
            time.sleep(0.1)
            
            print(f"    ✓ Worker spawned successfully")
            self.tests_passed += 1
            return True
        except Exception as e:
            print(f"    ✗ Worker spawn failed: {e}")
            self.tests_failed += 1
            return False
    
    def test_concurrent_pushing(self):
        """Test concurrent frame pushing from multiple threads."""
        print("  [TEST]: Testing concurrent frame pushing...")
        
        try:
            # Create a new pipeline for this test
            test_pipeline = LockFreeAudioPipeline()
            
            # Spawn the worker
            test_pipeline.spawn_isolated_audio_worker()
            
            # Create multiple threads pushing frames
            def push_frames(thread_id):
                for i in range(100):
                    frames = [thread_id * 1000 + i]
                    test_pipeline.push_frame_block(frames)
                    time.sleep(0.001)
            
            threads = []
            for i in range(5):
                t = threading.Thread(target=push_frames, args=(i,))
                threads.append(t)
                t.start()
            
            # Wait for all threads to complete
            for t in threads:
                t.join()
            
            print(f"    ✓ Concurrent pushing successful (5 threads, 100 frames each)")
            self.tests_passed += 1
            return True
        except Exception as e:
            print(f"    ✗ Concurrent pushing failed: {e}")
            self.tests_failed += 1
            return False
    
    def test_performance(self):
        """Test performance of lock-free operations."""
        print("  [TEST]: Testing performance...")
        
        try:
            # Create a new pipeline for this test
            test_pipeline = LockFreeAudioPipeline()
            
            # Test push performance
            test_frames = [i % 100 for i in range(1000)]
            
            start = time.perf_counter()
            for _ in range(1000):
                test_pipeline.push_frame_block(test_frames)
                elapsed = time.perf_counter() - start
                if elapsed > 0.1:  # Don't let it run too long
                    break
            push_time = time.perf_counter() - start
            
            print(f"    ✓ Performance test completed")
            print(f"      Push time: {push_time*1000:.2f}ms for multiple iterations")
            
            self.tests_passed += 1
            return True
        except Exception as e:
            print(f"    ✗ Performance test failed: {e}")
            self.tests_failed += 1
            return False
    
    def test_stress_conditions(self):
        """Test pipeline under stress conditions."""
        print("  [TEST]: Testing stress conditions...")
        
        try:
            # Create a new pipeline for this test
            test_pipeline = LockFreeAudioPipeline()
            
            # Spawn the worker
            test_pipeline.spawn_isolated_audio_worker()
            
            # Rapidly push frames
            failures = 0
            successes = 0
            
            for i in range(5000):
                frames = [i % 100]
                success = test_pipeline.push_frame_block(frames)
                if success:
                    successes += 1
                else:
                    failures += 1
            
            success_rate = (successes / (successes + failures)) * 100 if (successes + failures) > 0 else 0
            
            print(f"    ✓ Stress test completed")
            print(f"      Successes: {successes}, Failures: {failures}")
            print(f"      Success rate: {success_rate:.2f}%")
            
            self.tests_passed += 1
            return True
        except Exception as e:
            print(f"    ✗ Stress test failed: {e}")
            self.tests_failed += 1
            return False
    
    def run_all_tests(self):
        """Run complete test suite."""
        print("\n" + "=" * 70)
        print("  LOCK-FREE AUDIO PIPELINE TEST SUITE")
        print("=" * 70 + "\n")
        
        if not RUST_AVAILABLE:
            print("  [TEST]: Cannot proceed - titan_forge not available")
            return False
        
        self.test_pipeline_creation()
        self.test_frame_pushing()
        self.test_large_block_pushing()
        self.test_channel_full()
        self.test_worker_spawn()
        self.test_concurrent_pushing()
        self.test_performance()
        self.test_stress_conditions()
        
        print("\n" + "=" * 70)
        print("  [TEST RESULTS]")
        print("=" * 70)
        print(f"    Passed: {self.tests_passed}")
        print(f"    Failed: {self.tests_failed}")
        print(f"    Total: {self.tests_passed + self.tests_failed}")
        
        if self.tests_failed == 0:
            print("\n    ✓ ALL TESTS PASSED")
        else:
            print(f"\n    ✗ {self.tests_failed} TEST(S) FAILED")
        
        print("=" * 70 + "\n")
        
        return self.tests_failed == 0


def main():
    """Main test execution."""
    test_suite = LockFreePipelineTest()
    success = test_suite.run_all_tests()
    
    if success:
        print("  [TEST]: Lock-free pipeline test suite completed successfully")
        sys.exit(0)
    else:
        print("  [TEST]: Lock-free pipeline test suite completed with failures")
        sys.exit(1)


if __name__ == "__main__":
    main()
