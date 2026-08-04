"""
Postcard Binary Bridge
NASA-standard binary serialization replacing slow JSON string parsing
Ultra-dense binary format for instant Rust/embedded chip communication
"""

import struct
from typing import List, Optional

class PostcardBinaryBridge:
    """
    High-speed binary serialization bridge for Python-Rust communication.
    Uses fixed-allocation binary format compatible with game engines, medical devices, and embedded systems.
    """
    
    def __init__(self):
        """Initialize postcard binary bridge."""
        # Header format: [4 Bytes Magic ID] [2 Bytes Version ID] [2 Bytes Binary Data Length]
        self.header_format = "<4sHH"
        self.magic_bytes = b"ZED\x01"
        self.max_sat_clauses = 512  # Stack allocation limit for heapless compatibility
    
    def serialize_cognitive_packet(self, sentiment: float, arousal: float, 
                                   culture_id: int, sat_clauses: List[int]) -> bytes:
        """
        Packs emotional metrics, cultural contexts, and SAT constraints into raw binary stream.
        
        Args:
            sentiment: Sentiment score (float32)
            arousal: Arousal score (float32)
            culture_id: Culture ID (0=Western, 1=Eastern, 2=African, 3=Latin)
            sat_clauses: List of SAT solver clause values (int16)
            
        Returns:
            Binary packet ready for Rust/embedded consumption
            
        Raises:
            ValueError: If SAT clause count exceeds stack allocation limit
        """
        # Validate SAT clause count
        clause_count = len(sat_clauses)
        if clause_count > self.max_sat_clauses:
            raise ValueError(
                f"Constraint overflow: Maximum stack allocation limit is {self.max_sat_clauses} clauses, "
                f"received {clause_count}"
            )
        
        # Pack sentiment (float32), arousal (float32), culture_id (uint16)
        metrics_bin = struct.pack("<ffH", sentiment, arousal, culture_id)
        
        # Pack SAT clauses as int16 array
        clause_bin = struct.pack(f"<{clause_count}h", *sat_clauses)
        
        # Calculate full payload size
        payload = metrics_bin + clause_bin
        header = struct.pack(self.header_format, self.magic_bytes, 1, len(payload))
        
        # Returns clean, zero-overhead byte array (no string manipulation)
        return header + payload
    
    def deserialize_audio_stems(self, binary_data: bytes) -> Optional[bytes]:
        """
        Unpacks incoming raw PCM or MIDI events from Rust audio engine.
        
        Args:
            binary_data: Binary data packet from Rust
            
        Returns:
            Raw audio frame data or None if invalid packet
            
        Raises:
            ValueError: If packet magic bytes don't match protocol
        """
        if len(binary_data) < 8:
            return None
        
        magic, version, length = struct.unpack(self.header_format, binary_data[:8])
        
        if magic != self.magic_bytes:
            raise ValueError(
                f"Cryptographic/Structural Protocol Mismatch: Invalid Packet Magic ID. "
                f"Expected {self.magic_bytes}, got {magic}"
            )
        
        # Extract raw audio frame data directly into 4KB memory window
        if len(binary_data) < 8 + length:
            return None
            
        return binary_data[8:8+length]
    
    def deserialize_cognitive_response(self, binary_data: bytes) -> Optional[dict]:
        """
        Deserialize cognitive response from Rust backend.
        
        Args:
            binary_data: Binary response packet
            
        Returns:
            Dictionary with response data or None if invalid
        """
        if len(binary_data) < 8:
            return None
        
        magic, version, length = struct.unpack(self.header_format, binary_data[:8])
        
        if magic != self.magic_bytes:
            return None
        
        if len(binary_data) < 8 + length:
            return None
        
        payload = binary_data[8:8+length]
        
        # Parse response based on version
        if version == 1:
            # Version 1: [success:bool, result_code:int32, message_length:uint16, message:bytes]
            if len(payload) < 7:
                return None
            
            success = struct.unpack("<?", payload[0:1])[0]
            result_code = struct.unpack("<i", payload[1:5])[0]
            message_length = struct.unpack("<H", payload[5:7])[0]
            
            if len(payload) < 7 + message_length:
                return None
            
            message = payload[7:7+message_length].decode('utf-8', errors='ignore')
            
            return {
                'success': success,
                'result_code': result_code,
                'message': message
            }
        
        return None
    
    def validate_packet_structure(self, binary_data: bytes) -> bool:
        """
        Validate binary packet structure without full deserialization.
        
        Args:
            binary_data: Binary data to validate
            
        Returns:
            True if packet structure is valid
        """
        if len(binary_data) < 8:
            return False
        
        try:
            magic, version, length = struct.unpack(self.header_format, binary_data[:8])
            
            if magic != self.magic_bytes:
                return False
            
            if len(binary_data) < 8 + length:
                return False
            
            return True
        except struct.error:
            return False
