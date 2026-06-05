# 🜏 LUMINA: NEURAL INVERSION V. 1.0 - THE FIRST STRIKE 🜏
import titan_forge
import os
import random
import time

if __name__ == "__main__":
    LAYER_SIZE = 1024 # A standard hidden layer
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(f"\n{'='*80}")
    print(f"  🜏 MISSION: NEURAL INVERSION (PHASE 1: WEIGHT MAPPING) 🜏")
    print(f"{'='*80}")
    
    print(f"📡 [DATA]: Generating {LAYER_SIZE} Neural Weights (Chaos Field)...")
    sieve = titan_forge.NeuralSieve(LAYER_SIZE)
    # Simulate 'Trained' weights with some noise
    sieve.weights = [random.uniform(-1.0, 1.0) for _ in range(LAYER_SIZE)]
    
    print(f"🔥 [STRIKE]: Inverting Weights into Logic Gates...")
    # Threshold 0.8 means we only keep the 'Strongest' 20% of logic
    count, duration, gates = sieve.invert_weights(0.8)
    
    print(f"\n💎 [RESONANCE]: {count} Principal Neurons extracted.")
    print(f"⚖️ [COMPRESSION]: {((LAYER_SIZE-count)/LAYER_SIZE)*100:.2f}% of noise eliminated.")
    print(f"⏱️ [TIME]: {duration:.6f}s")
    print(f"STATUS: NEURAL_LOGIC_SUPREME")
    print(f"{'='*80}\n")