# EXECUTION LOG: ALCHEMICAL SENTINEL V.2.0
# TARGET: Ol-ad-aba (Oil of Father)
# CATALYST: Stibium (Antimony) Stabilization ACTIVE

from Lumina.sentinel import AlchemicalSentinel
import time

def execute_final_maceration():
    # 1. SETUP: The 1:3:7 Proportional Recipe (Folio 103R)
    # Using 9 variables representing the stabilized 9-bit key
    clauses = [[1, 2, 3], [-1, -4], [5, 6], [-2, -7], [8, 9], [4, -8]]
    var_count = 9
    
    print("🔥 [HEATING]: Initiating Thermal Stabilization (stones.py logic)...")
    sentinel = AlchemicalSentinel(clauses, var_count)
    
    start_time = time.time()
    
    # 2. THE SOLVE: Using Antimony to prune the search space
    if sentinel.solve():
        duration = time.time() - start_time
        print(f"✅ [RESONANCE]: 100% SYNCHRONICITY REACHED.")
        print(f"⏱️  [SPEED]: {duration:.8f}s (Previous: 0.0001000s)")
        
        # 3. VERDICT
        key = "".join(['1' if sentinel.assignment.get(i) else '0' for i in range(1, 10)])
        print(f"💎 [RESULT]: The 'Oil of Father' is VIVIFIED.")
        print(f"🔑 [MASTER KEY]: {key}")
    else:
        print("❌ [CONFLICT]: Thermal runaway detected. Vault remains sealed.")

if __name__ == "__main__":
    execute_final_maceration()
