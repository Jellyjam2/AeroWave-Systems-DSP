import titan_forge
import os
import random
import time

if __name__ == "__main__":
    VARS = 1000
    STEPS = 1_000_000  # THE MILLION-STEP SIEGE
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(f"{'='*70}")
    print(f"  🜏 MISSION: HEAT-DEATH SIEGE (1,000 VAR MANIFOLD) 🜏")
    print(f"{'='*75}")
    
    print(f"📡 [DATA]: Generating Critical-Ratio Manifold (4.26)...")
    # Generating the "Hard Wall" for the i3-4030U
    clauses = []
    for _ in range(int(VARS * 4.26)):
        v = random.sample(range(1, VARS + 1), 3)
        clauses.append([(v[i] if random.random() > 0.5 else -v[i]) for i in range(3)])
    
    print(f"🔥 [STRIKE]: Engaging Quad-Blade Annealer (1M Steps)...")
    print(f"🌡️ [STATUS]: TDP Redline. Parallel Reheating (Phoenix) Active.")
    
    # Initializing the Arc-wrapped General
    forge = titan_forge.OmegaAnnealer(VARS)
    
    start_time = time.time()
    success, energy, duration = forge.execute_omega_siege(clauses, STEPS)
    total_latency = time.time() - start_time
    
    print(f"\nRESULT: {'💎 WALL SHATTERED (SAT)' if success else '🌑 WALL HELD (UNSAT/MIN)'}")
    print(f"ENERGY: {energy} (Conflicts Remaining)")
    print(f"TIME: {duration:.4f}s (RUST-SPEED)")
    print(f"STATUS: LOGIC SUPREME")
    print(f"{'='*75}\n")