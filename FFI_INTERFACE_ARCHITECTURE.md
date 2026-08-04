# FFI Interface Architecture - Version 1.1

## **Overview**

The C-Compatible FFI (Foreign Function Interface) enables Titan Forge integration with game engines (Unreal Engine, Unity) and other native applications. This architecture provides a stable C ABI while maintaining NASA-grade Rust performance.

---

## **Architecture Layers**

```
┌─────────────────────────────────────────────────────────────┐
│                    Game Engine Layer                          │
│  ┌──────────────────┐         ┌──────────────────┐          │
│  │  Unreal Engine   │         │     Unity        │          │
│  │      (C++)       │         │     (C#)         │          │
│  └────────┬─────────┘         └────────┬─────────┘          │
└───────────┼───────────────────────────┼──────────────────────┘
            │                           │
            └───────────┬───────────────┘
                        │
┌───────────────────────┼───────────────────────────────────────┐
│              C-Compatible FFI Layer (titan_forge.h)           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  • Opaque handles for memory safety                  │   │
│  │  • Error codes for graceful degradation             │   │
│  │  • Version/capability queries                       │   │
│  └──────────────────────────────────────────────────────┘   │
└───────────────────────┼───────────────────────────────────────┘
                        │
┌───────────────────────┼───────────────────────────────────────┐
│              Rust Core (titan_forge)                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  • CognitivePayload (postcard binary bridge)        │   │
│  │  • LockFreeAudioPipeline (core affinity)             │   │
│  │  • MusicMatrix (nalgebra matrices)                  │   │
│  └──────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────┘
```

---

## **C Header Specification**

**File:** `include/titan_forge.h`

### **Error Codes**
```c
typedef enum {
    TITAN_FORGE_SUCCESS = 0,
    TITAN_FORGE_INVALID_HANDLE = 1,
    TITAN_FORGE_NULL_POINTER = 2,
    TITAN_FORGE_BUFFER_OVERFLOW = 3,
    TITAN_FORGE_INVALID_DATA = 4,
    TITAN_FORGE_INTERNAL_ERROR = 5
} TitanForgeError;
```

### **Opaque Handles**
```c
typedef struct CognitivePayloadHandle CognitivePayloadHandle;
typedef struct LockFreeAudioPipelineHandle LockFreeAudioPipelineHandle;
typedef struct MusicMatrixHandle MusicMatrixHandle;
```

### **Core Functions**

#### **Library Information**
```c
const char* titan_forge_get_version(void);
uint32_t titan_forge_get_capabilities(void);
const char* titan_forge_error_to_string(TitanForgeError error);
```

#### **CognitivePayload API**
```c
CognitivePayloadHandle* titan_forge_cognitive_payload_create(void);
TitanForgeError titan_forge_cognitive_payload_destroy(CognitivePayloadHandle* handle);
TitanForgeError titan_forge_cognitive_payload_unpack(
    CognitivePayloadHandle* handle,
    const uint8_t* data,
    size_t data_len,
    float* out_sentiment,
    float* out_arousal,
    uint16_t* out_culture_id,
    size_t* out_clauses_count
);
```

#### **LockFreeAudioPipeline API**
```c
LockFreeAudioPipelineHandle* titan_forge_lockfree_pipeline_create(void);
TitanForgeError titan_forge_lockfree_pipeline_destroy(LockFreeAudioPipelineHandle* handle);
TitanForgeError titan_forge_lockfree_pipeline_push(
    LockFreeAudioPipelineHandle* handle,
    const int16_t* frames,
    size_t frame_count
);
TitanForgeError titan_forge_lockfree_pipeline_spawn_worker(LockFreeAudioPipelineHandle* handle);
```

#### **MusicMatrix API**
```c
MusicMatrixHandle* titan_forge_music_matrix_create(void);
TitanForgeError titan_forge_music_matrix_destroy(MusicMatrixHandle* handle);
TitanForgeError titan_forge_music_matrix_create_pitch(
    MusicMatrixHandle* handle,
    const float* emotional_vector,
    size_t vector_len
);
```

---

## **Build Configuration**

### **Rust Cargo.toml (v1.1)**
```toml
[lib]
name = "titan_forge"
crate-type = ["cdylib", "rlib"]  # Both C library and Rust library
```

### **Separate Build Targets**
- **Python Extension:** `maturin develop` (current v1.0)
- **C Library:** `cargo build --release --lib` (v1.1 addition)

---

## **Game Engine Integration**

### **Unreal Engine (C++)**

**Wrapper Class:**
```cpp
// TitanForgeUnreal.h
#pragma once

#include "CoreMinimal.h"
#include "titan_forge.h"
#include "TitanForgeUnreal.generated.h"

UCLASS()
class TITANFORGE_API UTitanForgeUnreal : public UObject
{
    GENERATED_BODY()

public:
    // Initialize Titan Forge
    bool Initialize();
    
    // Process audio frames
    bool ProcessAudio(const TArray<int16>& Frames);
    
    // Generate music from emotional vector
    bool GenerateMusic(const TArray<float>& EmotionalVector);
    
    // Get version
    FString GetVersion();
    
private:
    CognitivePayloadHandle* PayloadHandle;
    LockFreeAudioPipelineHandle* AudioHandle;
    MusicMatrixHandle* MatrixHandle;
};
```

### **Unity (C#)**

**Wrapper Class:**
```csharp
// TitanForgeUnity.cs
using System;
using System.Runtime.InteropServices;

public class TitanForgeUnity : IDisposable
{
    // Import FFI functions
    [DllImport("titan_forge")]
    private static extern IntPtr titan_forge_cognitive_payload_create();
    
    [DllImport("titan_forge")]
    private static extern int titan_forge_cognitive_payload_destroy(IntPtr handle);
    
    [DllImport("titan_forge")]
    private static extern int titan_forge_lockfree_pipeline_push(
        IntPtr handle, 
        IntPtr frames, 
        UIntPtr frameCount
    );
    
    // Wrapper methods
    private IntPtr payloadHandle;
    private IntPtr audioHandle;
    
    public bool Initialize()
    {
        payloadHandle = titan_forge_cognitive_payload_create();
        return payloadHandle != IntPtr.Zero;
    }
    
    public bool ProcessAudio(short[] frames)
    {
        // Pin array and send to Rust
        GCHandle handle = GCHandle.Alloc(frames, GCHandleType.Pinned);
        try
        {
            IntPtr framePtr = handle.AddrOfPinnedObject();
            int result = titan_forge_lockfree_pipeline_push(
                audioHandle, 
                framePtr, 
                (UIntPtr)frames.Length
            );
            return result == 0; // TITAN_FORGE_SUCCESS
        }
        finally
        {
            handle.Free();
        }
    }
    
    public void Dispose()
    {
        if (payloadHandle != IntPtr.Zero)
        {
            titan_forge_cognitive_payload_destroy(payloadHandle);
            payloadHandle = IntPtr.Zero;
        }
    }
}
```

---

## **Memory Safety Protocol**

### **Ownership Model**
- **Rust owns all internal data structures**
- **C/C#/C++ receives opaque handles only**
- **No direct memory access across FFI boundary**
- **Automatic cleanup via destroy functions**

### **Error Handling**
- **All functions return error codes**
- **Null pointer checks before dereferencing**
- **Graceful degradation on errors**
- **No panics across FFI boundary**

---

## **Performance Considerations**

### **Zero-Copy Where Possible**
- **Audio frames:** Direct pointer access (no copying)
- **Binary packets:** Postcard serialization (minimal overhead)
- **Matrix operations:** In-place nalgebra computations

### **Thread Safety**
- **Lock-free channels:** No mutex contention
- **Core affinity:** Isolated audio worker on Core 1
- **No GIL:** Native OS threads (bypassing Python)

---

## **Version 1.1 Implementation Plan**

### **Phase 1: Build Configuration**
1. Add `cdylib` to `Cargo.toml`
2. Create separate build script for C library
3. Generate platform-specific binaries (.dll, .so, .dylib)

### **Phase 2: FFI Implementation**
1. Complete all FFI functions in `src/lib.rs`
2. Add comprehensive error handling
3. Implement opaque handle management
4. Add memory safety checks

### **Phase 3: Game Engine Wrappers**
1. Create C++ wrapper for Unreal Engine
2. Create C# wrapper for Unity
3. Write integration examples
4. Create plugin packages

### **Phase 4: Documentation**
1. API reference documentation
2. Integration guides for each engine
3. Performance benchmarks
4. Troubleshooting guide

---

## **Testing Strategy**

### **Unit Tests**
- **FFI function correctness**
- **Error code propagation**
- **Memory leak detection**

### **Integration Tests**
- **Unreal Engine plugin loading**
- **Unity C# interop**
- **Cross-platform binary compatibility**

### **Performance Tests**
- **FFI overhead measurement**
- **Audio frame throughput**
- **Matrix operation latency**

---

## **Deployment**

### **Distribution**
- **Binaries:** Platform-specific shared libraries
- **Headers:** `titan_forge.h` for C/C++
- **Wrappers:** Engine-specific plugin packages
- **Documentation:** Integration guides and API reference

### **Versioning**
- **Semantic versioning for FFI API**
- **Backward compatibility guarantees**
- **Deprecation warnings for breaking changes**

---

*This FFI architecture enables Titan Forge to integrate with game engines while maintaining NASA-grade performance and memory safety.*
