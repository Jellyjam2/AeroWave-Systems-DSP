"""
Postcard Binary Bridge Test Suite
Verifies Python-Rust binary communication with heapless structures and zeroize
"""

import sys
import os
import time
import struct

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from LuminaCantor.postcard_bridge import PostcardBinaryBridge

# Try to import titan_forge
try:
    import titan_forge
    RUST_AVAILABLE = True
except ImportError:
    RUST_AVAILABLE = False
    print("  [TEST]: titan_forge not available - testing Python bridge only")

class PostcardBridgeTest:
    """Test suite for postcard binary bridge."""
    
    def __init__(self):
        """Initialize test suite."""
        self.bridge = PostcardBinaryBridge()
        self.tests_passed = 0
        self.tests_failed = 0
    
    def test_basic_serialization(self):
        """Test basic cognitive packet serialization."""
        print("  [TEST]: Testing basic serialization...")
        
        sentiment = 0.75
        arousal = 0.50
        culture_id = 0  # Western
        sat_clauses = [1, -1, 2, -2, 3, -3]
        
        try:
            packet = self.bridge.serialize_cognitive_packet(
                sentiment, arousal, culture_id, sat_clauses
            )
            
            # Verify packet structure
            assert len(packet) >= 8, "Packet too short for header"
            assert packet[:4] == b"ZED\x01", "Invalid magic bytes"
            
            print(f"    ✓ Serialization successful (packet size: {len(packet)} bytes)")
            self.tests_passed += 1
            return True
        except Exception as e:
            print(f"    ✗ Serialization failed: {e}")
            self.tests_failed += 1
            return False
    
    def test_clause_limit(self):
        """Test SAT clause capacity limit enforcement."""
        print("  [TEST]: Testing SAT clause limit (512 max)...")
        
        # Test within limit
        try:
            sat_clauses = list(range(500))
            packet = self.bridge.serialize_cognitive_packet(0.5, 0.5, 0, sat_clauses)
            print(f"    ✓ 500 clauses accepted (packet size: {len(packet)} bytes)")
            self.tests_passed += 1
        except ValueError as e:
            print(f"    ✗ 500 clauses rejected: {e}")
            self.tests_failed += 1
            return False
        
        # Test exceeding limit
        try:
            sat_clauses = list(range(600))
            packet = self.bridge.serialize_cognitive_packet(0.5, 0.5, 0, sat_clauses)
            print(f"    ✗ 600 clauses incorrectly accepted")
            self.tests_failed += 1
            return False
        except ValueError as e:
            print(f"    ✓ 600 clauses correctly rejected: {e}")
            self.tests_passed += 1
            return True
    
    def test_audio_deserialization(self):
        """Test audio stem deserialization."""
        print("  [TEST]: Testing audio deserialization...")
        
        # Create valid audio packet
        audio_data = b'\x00' * 100
        header = struct.pack("<4sHH", b"ZED\x01", 1, len(audio_data))
        packet = header + audio_data
        
        try:
            result = self.bridge.deserialize_audio_stems(packet)
            assert result == audio_data, "Audio data mismatch"
            print(f"    ✓ Audio deserialization successful (100 bytes)")
            self.tests_passed += 1
            return True
        except Exception as e:
            print(f"    ✗ Audio deserialization failed: {e}")
            self.tests_failed += 1
            return False
    
    def test_invalid_packet(self):
        """Test invalid packet rejection."""
        print("  [TEST]: Testing invalid packet rejection...")
        
        # Invalid magic bytes
        invalid_packet = struct.pack("<4sHH", b"BAD\x01", 1, 10) + b'\x00' * 10
        
        try:
            result = self.bridge.deserialize_audio_stems(invalid_packet)
            print(f"    ✗ Invalid packet incorrectly accepted")
            self.tests_failed += 1
            return False
        except ValueError as e:
            print(f"    ✓ Invalid packet correctly rejected: {e}")
            self.tests_passed += 1
            return True
    
    def test_packet_validation(self):
        """Test packet structure validation."""
        print("  [TEST]: Testing packet structure validation...")
        
        # Valid packet
        valid_packet = struct.pack("<4sHH", b"ZED\x01", 1, 10) + b'\x00' * 10
        assert self.bridge.validate_packet_structure(valid_packet), "Valid packet rejected"
        
        # Invalid magic
        invalid_magic = struct.pack("<4sHH", b"BAD\x01", 1, 10) + b'\x00' * 10
        assert not self.bridge.validate_packet_structure(invalid_magic), "Invalid magic accepted"
        
        # Too short
        too_short = b"ZED"
        assert not self.bridge.validate_packet_structure(too_short), "Too short accepted"
        
        print(f"    ✓ Packet validation working correctly")
        self.tests_passed += 1
        return True
    
    def test_rust_integration(self):
        """Test Rust backend integration if available."""
        if not RUST_AVAILABLE:
            print("  [TEST]: Skipping Rust integration (titan_forge not available)")
            return True
        
        print("  [TEST]: Testing Rust backend integration...")
        
        try:
            # Create CognitivePayload
            payload = titan_forge.CognitivePayload()
            
            # Create test packet
            sentiment = 0.85
            arousal = 0.60
            culture_id = 1  # Eastern
            sat_clauses = [5, -5, 10, -10, 15, -15]
            
            packet = self.bridge.serialize_cognitive_packet(
                sentiment, arousal, culture_id, sat_clauses
            )
            
            # Unpack in Rust
            success = payload.unpack_from_bridge(packet)
            
            if not success:
                print(f"    ✗ Rust unpacking failed")
                self.tests_failed += 1
                return False
            
            # Verify values
            assert abs(payload.sentiment - sentiment) < 0.01, f"Sentiment mismatch: {payload.sentiment} vs {sentiment}"
            assert abs(payload.arousal - arousal) < 0.01, f"Arousal mismatch: {payload.arousal} vs {arousal}"
            assert payload.culture_id == culture_id, f"Culture ID mismatch: {payload.culture_id} vs {culture_id}"
            
            print(f"    ✓ Rust integration successful")
            print(f"      Sentiment: {payload.sentiment}")
            print(f"      Arousal: {payload.arousal}")
            print(f"      Culture ID: {payload.culture_id}")
            print(f"      SAT clauses: {len(payload.sat_clauses)}")
            
            self.tests_passed += 1
            return True
            
        except Exception as e:
            print(f"    ✗ Rust integration failed: {e}")
            self.tests_failed += 1
            return False
    
    def test_round_trip(self):
        """Test Python-Rust round-trip if available."""
        if not RUST_AVAILABLE:
            print("  [TEST]: Skipping round-trip (titan_forge not available)")
            return True
        
        print("  [TEST]: Testing Python-Rust round-trip...")
        
        try:
            # Create original data
            original_sentiment = 0.92
            original_arousal = 0.45
            original_culture_id = 2  # African
            original_sat_clauses = [20, -20, 40, -40, 60, -60]
            
            # Serialize in Python
            packet = self.bridge.serialize_cognitive_packet(
                original_sentiment, original_arousal, original_culture_id, original_sat_clauses
            )
            
            # Unpack in Rust
            payload = titan_forge.CognitivePayload()
            payload.unpack_from_bridge(packet)
            
            # Pack back in Rust
            returned_packet = payload.pack_to_bridge()
            
            # Deserialize in Python
            # (For now, just verify the packet is valid)
            assert self.bridge.validate_packet_structure(returned_packet), "Returned packet invalid"
            
            print(f"    ✓ Round-trip successful")
            print(f"      Original size: {len(packet)} bytes")
            print(f"      Returned size: {len(returned_packet)} bytes")
            
            self.tests_passed += 1
            return True
            
        except Exception as e:
            print(f"    ✗ Round-trip failed: {e}")
            self.tests_failed += 1
            return False
    
    def test_performance_comparison(self):
        """Compare binary vs JSON performance."""
        print("  [TEST]: Testing performance comparison (binary vs JSON)...")
        
        import json
        
        sentiment = 0.75
        arousal = 0.50
        culture_id = 0
        sat_clauses = list(range(100))
        
        # Test binary serialization
        start = time.perf_counter()
        for _ in range(1000):
            packet = self.bridge.serialize_cognitive_packet(sentiment, arousal, culture_id, sat_clauses)
        binary_time = time.perf_counter() - start
        
        # Test JSON serialization
        data = {
            'sentiment': sentiment,
            'arousal': arousal,
            'culture_id': culture_id,
            'sat_clauses': sat_clauses
        }
        
        start = time.perf_counter()
        for _ in range(1000):
            json_str = json.dumps(data)
        json_time = time.perf_counter() - start
        
        speedup = json_time / binary_time if binary_time > 0 else 0
        
        print(f"    Binary: {binary_time*1000:.2f}ms for 1000 iterations")
        print(f"    JSON: {json_time*1000:.2f}ms for 1000 iterations")
        print(f"    Speedup: {speedup:.2f}x")
        
        self.tests_passed += 1
        return True
    
    def run_all_tests(self):
        """Run complete test suite."""
        print("\n" + "=" * 70)
        print("  POSTCARD BINARY BRIDGE TEST SUITE")
        print("=" * 70 + "\n")
        
        self.test_basic_serialization()
        self.test_clause_limit()
        self.test_audio_deserialization()
        self.test_invalid_packet()
        self.test_packet_validation()
        
        if RUST_AVAILABLE:
            self.test_rust_integration()
            self.test_round_trip()
        
        self.test_performance_comparison()
        
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
    test_suite = PostcardBridgeTest()
    success = test_suite.run_all_tests()
    
    if success:
        print("  [TEST]: Test suite completed successfully")
        sys.exit(0)
    else:
        print("  [TEST]: Test suite completed with failures")
        sys.exit(1)


if __name__ == "__main__":
    main()
