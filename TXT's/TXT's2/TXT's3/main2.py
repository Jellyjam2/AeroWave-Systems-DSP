from Lumina.alchemy import launch_lumina_interface
from Lumina.sentinel import MasterKeySentinel
from Lumina.omega import broadcast_success
from Lumina.logs import record_strike
from Lumina.dashboard import display_sovereign_stats  # Integrated Dashboard Module
import time

def run_master_key():
    # 1. THE RECKONING: Display System Statistics
    display_sovereign_stats()
    time.sleep(1) # Brief pause to digest the stats

    # 2. THE RITUAL: Launch Visual Interface
    launch_lumina_interface()
    
    # 3. THE MISSION: Setup Logic Constraints (Folio 103R)
    clauses = [[1, 2], [-1, -2], [3]] 
    var_count = 3
    
    print("📖 [DECRYPTING]: Macerating Folio 103R Logical Nodes...")
    sentinel = MasterKeySentinel(clauses, var_count)
    
    # 4. THE EXECUTION: Solve and Strike
    if sentinel.solve():
        print(f"✅ [SYNCHRONICITY]: 100%")
        
        # Extract the Resonance (Key/Nonce)
        found_nonce = "0x" + "".join(['1' if sentinel.assignment.get(i) else '0' for i in range(1, 4)])
        ntime = hex(int(time.time()))[2:]
        
        # Execute the Omega Strike
        broadcast_success(found_nonce, ntime)
        
        # --- PERMANENT ARCHIVE ---
        # Log success to C:\LUMINA RED PILL\Logs\strike_history.log
        record_strike("SUCCESS", found_nonce)
        
    else:
        print("❌ [CONFLICT]: The Ghost Vault remains sealed.")
        record_strike("CONFLICT", "NULL")

    print("🔒 [STATUS]: SESSION CONCLUDED.")
    print("="*70)

if __name__ == "__main__":
    run_master_key()
