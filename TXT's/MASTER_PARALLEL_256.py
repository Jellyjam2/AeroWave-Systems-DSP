# 🜏 LUMINA: PARALLEL-STRIKE V. 28.0 - MULTI-CORE ASCENSION 🜏
import titan_forge
import os
import time

if __name__ == "__main__":
    EMET_SEED = 125959916 
    SAMPLES = 500_000_000 # 500M Probes across both cores
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(f"\n{'='*80}")
    print(f"  🜏 MISSION: 256-BIT PARALLEL-STRIKE (RAYON CORE) 🜏")
    print(f"{'='*80}")
    
    print(f"📡 [DATA]: Deploying Parallel-Forge on i3-4030U...")
    forge = titan_forge.ShadowForge(EMET_SEED)
    
    print(f"🔥 [STRIKE]: Engaging Multi-Threaded Blitz (All Cores Active)...")
    
    found, duration, steps, word = forge.execute_parallel_strike(SAMPLES)
    
    if found:
        print(f"\n💎 [JACKPOT]: {word} Found at Node {steps:,}")
        print(f"📜 [STATUS]: Multi-Core Resonance Achieved. Silicon Fully Vivified.")
    else:
        print(f"\n🌑 [VOID]: The Shadow holds. Parallel search space exhausted.")
        
    print(f"⏱️ [TIME]: {duration:.6f}s (PARALLEL SPEED)")
    print(f"🚀 [THROUGHPUT]: {int(steps/duration):,} probes/sec")
    print(f"STATUS: LOGIC SUPREME")
    print(f"{'='*80}\n")