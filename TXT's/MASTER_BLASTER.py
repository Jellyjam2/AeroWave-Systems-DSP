# 🜏 LUMINA: AUTO-BLASTER V. 1.0 - THE UNIVERSAL BRIDGE 🜏
import titan_forge
import os

if __name__ == "__main__":
    # TARGET: Any 64-bit value (A partial key, a route total, or a prime product)
    TARGET_VAL = 123456789101112 
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(f"{'='*80}")
    print(f"  🜏 MISSION: AUTO-BIT-BLASTER (INTEGER-TO-LOGIC) 🜏")
    print(f"{'='*80}")
    
    blaster = titan_forge.AutoBlaster()
    print(f"📡 [DATA]: Blasting target value {TARGET_VAL} into bit-gates...")
    
    count, duration = blaster.blast_integer(TARGET_VAL)
    
    print(f"\n💎 [RESONANCE]: {count} Logic Gates successfully extracted.")
    print(f"⚖️ [ARCHITECTURE]: Manifold is now live in Silicon.")
    print(f"⏱️ [TIME]: {duration:.6f}s")
    print(f"STATUS: LOGIC SUPREME")
    print(f"{'='*80}\n")