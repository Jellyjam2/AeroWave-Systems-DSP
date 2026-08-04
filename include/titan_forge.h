/**
 * AeroWave Systems DSP - C-Compatible Interface
 * Version 1.0.0
 * 
 * Copyright 2026 AeroWave Systems DSP
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * High-performance music generation engine with NASA-grade architecture
 * Compatible with Unreal Engine (C++), Unity (C#), and other game engines
 */

#ifndef AEROWAVE_DSP_H
#define AEROWAVE_DSP_H

#include <stdint.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

// ============================================================================
// Error Codes
// ============================================================================

typedef enum {
    AEROWAVE_SUCCESS = 0,
    AEROWAVE_INVALID_HANDLE = 1,
    AEROWAVE_NULL_POINTER = 2,
    AEROWAVE_BUFFER_OVERFLOW = 3,
    AEROWAVE_INVALID_DATA = 4,
    AEROWAVE_INTERNAL_ERROR = 5
} AeroWaveError;

// ============================================================================
// Opaque Handles (Forward Declarations)
// ============================================================================

typedef struct CognitivePayloadHandle CognitivePayloadHandle;
typedef struct LockFreeAudioPipelineHandle LockFreeAudioPipelineHandle;
typedef struct MusicMatrixHandle MusicMatrixHandle;

// ============================================================================
// Library Information
// ============================================================================

/**
 * Get library version string
 * @returns Static string containing version (e.g., "1.0.0")
 */
const char* aerowave_get_version(void);

/**
 * Get library capabilities as bit flags
 * @returns Bit flags indicating available features:
 *          Bit 0: Postcard binary bridge
 *          Bit 1: Lock-free audio pipeline
 *          Bit 2: Matrix-based music theory
 *          Bit 3: Heapless memory structures
 *          Bit 4: Zeroize memory scrubbing
 */
uint32_t aerowave_get_capabilities(void);

// ============================================================================
// CognitivePayload API
// ============================================================================

/**
 * Create a new CognitivePayload instance
 * @returns Handle to the new instance, or NULL on failure
 */
CognitivePayloadHandle* aerowave_cognitive_payload_create(void);

/**
 * Destroy a CognitivePayload instance
 * @param handle Handle to the instance to destroy
 * @returns Error code (AEROWAVE_SUCCESS on success)
 */
AeroWaveError aerowave_cognitive_payload_destroy(CognitivePayloadHandle* handle);

/**
 * Unpack binary packet into CognitivePayload
 * @param handle Handle to the CognitivePayload instance
 * @param data Pointer to binary data
 * @param data_lenLength of binary data in bytes
 * @param out_sentiment Output pointer for sentiment value (0.0 to 1.0)
 * @param out_arousal Output pointer for arousal value (0.0 to 1.0)
 * @param out_culture_id Output pointer for culture ID (0-3)
 * @param out_clauses_count Output pointer for number of SAT clauses
 * @returns Error code (AEROWAVE_SUCCESS on success)
 */
AeroWaveError aerowave_cognitive_payload_unpack(
    CognitivePayloadHandle* handle,
    const uint8_t* data,
    size_t data_len,
    float* out_sentiment,
    float* out_arousal,
    uint16_t* out_culture_id,
    size_t* out_clauses_count
);

// ============================================================================
// LockFreeAudioPipeline API
// ============================================================================

/**
 * Create a new LockFreeAudioPipeline instance
 * @returns Handle to the new instance, or NULL on failure
 */
LockFreeAudioPipelineHandle* aerowave_lockfree_pipeline_create(void);

/**
 * Destroy a LockFreeAudioPipeline instance
 * @param handle Handle to the instance to destroy
 * @returns Error code (AEROWAVE_SUCCESS on success)
 */
AeroWaveError aerowave_lockfree_pipeline_destroy(LockFreeAudioPipelineHandle* handle);

/**
 * Push audio frames into lock-free pipeline
 * @param handle Handle to the LockFreeAudioPipeline instance
 * @param frames Pointer to audio frame data (int16 samples)
 * @param frame_count Number of frames to push
 * @returns Error code (AEROWAVE_SUCCESS on success, AEROWAVE_BUFFER_OVERFLOW if full)
 */
AeroWaveError aerowave_lockfree_pipeline_push(
    LockFreeAudioPipelineHandle* handle,
    const int16_t* frames,
    size_t frame_count
);

/**
 * Spawn isolated audio worker thread
 * @param handle Handle to the LockFreeAudioPipeline instance
 * @returns Error code (AEROWAVE_SUCCESS on success)
 */
AeroWaveError aerowave_lockfree_pipeline_spawn_worker(LockFreeAudioPipelineHandle* handle);

// ============================================================================
// MusicMatrix API
// ============================================================================

/**
 * Create a new MusicMatrix instance
 * @returns Handle to the new instance, or NULL on failure
 */
MusicMatrixHandle* aerowave_music_matrix_create(void);

/**
 * Destroy a MusicMatrix instance
 * @param handle Handle to the instance to destroy
 * @returns Error code (AEROWAVE_SUCCESS on success)
 */
AeroWaveError aerowave_music_matrix_destroy(MusicMatrixHandle* handle);

/**
 * Create pitch transition matrix from emotional vector
 * @param handle Handle to the MusicMatrix instance
 * @param emotional_vector Pointer to emotional vector data (float array)
 * @param vector_len Length of emotional vector
 * @returns Error code (AEROWAVE_SUCCESS on success)
 */
AeroWaveError aerowave_music_matrix_create_pitch(
    MusicMatrixHandle* handle,
    const float* emotional_vector,
    size_t vector_len
);

// ============================================================================
// Utility Functions
// ============================================================================

/**
 * Convert error code to human-readable string
 * @param error Error code to convert
 * @returns Static string describing the error
 */
const char* aerowave_error_to_string(AeroWaveError error);

#ifdef __cplusplus
}
#endif

#endif // AEROWAVE_DSP_H
