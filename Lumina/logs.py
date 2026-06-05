import os
import datetime

# This points to the 'Logs' folder in your root directory
LOG_DIR = "Logs"

def record_strike(status, result_key):
    # Ensure the Logs folder exists
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] STATUS: {status} | KEY: {result_key}\n"
    
    # Append the entry to the master log file
    with open(os.path.join(LOG_DIR, "strike_history.log"), "a", encoding="utf-8") as f:
        f.write(log_entry)
    
    print(f"📜 [ARCHIVED]: Entry secured in {LOG_DIR}/strike_history.log")
