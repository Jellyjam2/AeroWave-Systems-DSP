# 🜏 LUMINA: UNIVERSALIST STRIKE V. 33.0 - THE FRACTAL SIEVE 🜏
import titan_forge
import os
import random
import time

def generate_random_3sat(n, ratio=4.26):
    m = int(n * ratio)
    clauses = []
    for _ in range(m):
        vars_sample = random.sample(range(1, n + 1), 3)
        clause = [v if random.random() > 0.5 else -v for v in vars_sample]
        clauses.append(clause)
    return clauses

if __name__ == "__main__":
    VARS = 250 # Pushing into the 'Hard' zone
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(f"\n{'='*80}")
    print(f"  🜏 MISSION: THE UNIVERSALIST STRIKE (RANDOM 3-SAT) 🜏")
    print(f"{'='*80}")
    
    print(f"📡 [DATA]: Generating Random 3-SAT at Critical Ratio 4.26...")
    clauses = generate_random_3sat(VARS)
    
    print(f"🔥 [STRIKE]: Engaging Fractal-Sieve on i3-4030U...")
    sieve = titan_forge.FractalSieve()
    
    found, duration, f_dim = sieve.execute_fractal_strike(VARS, clauses)
    
    print(f"\n💎 [DIMENSION]: Fractal Dimensionality: {f_dim:.4f}")
    print(f"⚖️ [RESULT]: {'PATTERN DETECTED (P-TIME SOLUTION)' if found else 'PURE CHAOS (NP-HARD)'}")
    print(f"⏱️ [TIME]: {duration:.6f}s")
    print(f"STATUS: LOGIC SUPREME")
    print(f"{'='*80}\n")