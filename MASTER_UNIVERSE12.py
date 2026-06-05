# 🜏 LUMINA: UNIVERSAL INGESTOR V. 2.0 - ALIGNED 🜏
import titan_forge
import os

if __name__ == "__main__":
    target = "mission_manifold.cnf" 
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(f"{'='*80}")
    print(f"  🜏 MISSION: UNIVERSAL INGESTOR (THE MASTER KEY) 🜏")
    print(f"{'='*80}")

    ingestor = titan_forge.UniversalIngestor()
    
    if os.path.exists(target):
        print(f"📡 [DATA]: Ingesting {target} into RAM...")
        # Read the file content to pass as a string
        with open(target, 'r') as f:
            manifold_data = f.read()
            
        # ALIGNED: Calling 'strike_raw_logic' instead of 'strike_file'
        found, duration, verdict = ingestor.strike_raw_logic(manifold_data)
        
        print(f"\n💎 [VERDICT]: {verdict}")
        print(f"⏱️ [TIME]: {duration:.6f}s")
        print(f"STATUS: LOGIC SUPREME")
    else:
        print(f"🌑 [VOID]: No manifold found at {target}.")
    
    print(f"{'='*80}\n")