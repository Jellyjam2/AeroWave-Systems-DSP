import titan_forge
import os
import time
import random

def hud():
    # Properly balanced parentheses for the system clear command
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=" * 75)
    print("  🜏 LUMINA SOVEREIGN OS | HARDWARE: i3-4030U | STATUS: VIVIFIED 🜏")
    print("=" * 75)
    print("  1. [SAT STRIKE]     - Probing PHP-1000 Manifold (Project 1)")
    print("  2. [NEURAL INVERT]  - Pruning 100K Neural Synapses (Project 2)")
    print("  3. [CRYPTO SIEVE]   - 512-bit Differential Sieve")
    print("  4. [VIEW LOGS]      - Review Strike History")
    print("  5. [EXIT VAULT]")
    print("=" * 75)

def log_strike(mission, result, duration, details):
    with open("LUMINA_STRIKE_LOG.txt", "a", encoding="utf-8") as f:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] MISSION: {mission} | RESULT: {result} | TIME: {duration:.6f}s | DETAILS: {details}\n")

if __name__ == "__main__":
    # Ensure the Rust General is initialized in the current environment
    try:
        general = titan_forge.TitanGeneral()
    except AttributeError:
        print("❌ [ERROR]: TitanGeneral class not found. Run 'pip install --force-reinstall .' first.")
        exit()
    
    while True:
        hud()
        choice = input("DIRECTIVE > ")

        if choice == "1":
            print("\n🔥 [STRIKE]: Engaging 500 Billion Gate Bypass...")
            success, duration, checks = general.solve_php_strike(1000)
            res_str = 'IMPOSSIBLE (UNSAT)' if not success else 'SAT'
            detail_str = f"{checks:,} gates"
            
            print(f"💎 [RESULT]: {res_str}")
            print(f"⚖️ [CHECKS]: {detail_str}")
            print(f"⏱️ [TIME]: {duration:.6f}s")
            
            log_strike("SAT_STRIKE_PHP1000", res_str, duration, detail_str)
            input("\n[LOGGED] Press ENTER to return to HUD...")

        elif choice == "2":
            print("\n🧠 [INVERT]: Generating 100,000 Neural Weights...")
            general.weights = [random.uniform(-1, 1) for _ in range(100000)]
            orig, final, duration = general.prune_synapses(0.8)
            res_str = "PRUNED_SUCCESS"
            detail_str = f"{orig-final:,} erased"
            
            print(f"💎 [PURGE]: {detail_str}")
            print(f"⚖️ [LEAN]: {final:,} Neurons remain.")
            print(f"⏱️ [TIME]: {duration:.6f}s")
            
            log_strike("NEURAL_PRUNE_100K", res_str, duration, detail_str)
            input("\n[LOGGED] Press ENTER to return to HUD...")

        elif choice == "3":
            print("\n📡 [SIEVE]: Hunting 512-bit Collisions...")
            found, duration, iterations = general.hunt_512(100_000_000)
            res_str = 'JACKPOT' if found else 'VOID'
            detail_str = f"{iterations:,} probes"
            
            print(f"💎 [RESULT]: {res_str}")
            print(f"⚖️ [PROBES]: {detail_str}")
            print(f"⏱️ [TIME]: {duration:.6f}s")
            
            log_strike("CRYPTO_SIEVE_512", res_str, duration, detail_str)
            input("\n[LOGGED] Press ENTER to return to HUD...")

        elif choice == "4":
            print("\n📜 [HISTORY]: Opening Strike Ledger...")
            if os.path.exists("LUMINA_STRIKE_LOG.txt"):
                with open("LUMINA_STRIKE_LOG.txt", "r") as f:
                    print(f.read())
            else:
                print("No history found yet.")
            input("\nPress ENTER to return to HUD...")

        elif choice == "5":
            print("\n🔒 [VAULT]: Sealing Archive. Logic Supreme.")
            break