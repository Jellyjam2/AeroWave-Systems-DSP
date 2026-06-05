import os

LOG_FILE = "Logs/strike_history.log"

def display_sovereign_stats():
    if not os.path.exists(LOG_FILE):
        print("📊 [DASHBOARD]: No history found in the Vault.")
        return

    with open(LOG_FILE, "r") as f:
        lines = f.readlines()

    total_strikes = len(lines)
    successes = sum(1 for line in lines if "STATUS: SUCCESS" in line)
    
    print("-" * 70)
    print(f"📊 [DASHBOARD]: LUMINA SYSTEM OVERVIEW")
    print(f"   [+] TOTAL SESSIONS: {total_strikes}")
    print(f"   [+] SUCCESSFUL RESONANCES: {successes}")
    print(f"   [+] STRIKE RATIO: {(successes/total_strikes)*100:.1f}%")
    
    if total_strikes > 0:
        print(f"   [+] LAST RECORDED KEY: {lines[-1].split('|')[-1].strip()}")
    print("-" * 70)
