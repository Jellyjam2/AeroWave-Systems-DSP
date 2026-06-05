# 🜏 LUMINA: NEURAL INVERSION V. 2.0 - ATOMIC PRUNING 🜏
import titan_forge
import os
import random
import time

if __name__ == "__main__":
    LAYER_SIZE = 100_000 # Scaling to 100K Neurons to test the Pruning speed
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(f"\n{'='*80}")
    print(f"  🜏 MISSION: ATOMIC PRUNING (PHASE 2: SYNAPTIC DELETION) 🜏")
    print(f"{'='*80}")
    
    print(f"📡 [DATA]: Initializing {LAYER_SIZE:,} Neurons...")
    sieve = titan_forge.NeuralSieve(LAYER_SIZE)
    sieve.weights = [random.uniform(-1.0, 1.0) for _ in range(LAYER_SIZE)]
    
    print(f"🔥 [STRIKE]: Executing Atomic Pruning (Threshold 0.8)...")
    
    orig, final, duration = sieve.prune_synapses(0.8)
    
    print(f"\n💎 [PURGE]: {orig - final:,} Synapses erased from Silicon.")
    print(f"⚖️ [LEAN STATE]: {final:,} Neurons remaining in the Core.")
    print(f"⏱️ [TIME]: {duration:.6f}s")
    print(f"STATUS: SILICON_OPTIMIZED")
    print(f"{'='*80}\n")