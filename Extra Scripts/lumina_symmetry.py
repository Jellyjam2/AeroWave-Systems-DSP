# 🜏 LUMINA: ZERO-POINT FORGE V. 9.0 - THE EQUILIBRIUM CORE 🜏
import tkinter as tk
from tkinter import scrolledtext
import threading
import time
import os
import datetime
import random
import titan_forge 

# --- 1. ARCHIVAL ENGINE ---
LOG_DIR = "Logs"
LOG_FILE = os.path.join(LOG_DIR, "strike_history.log")
if not os.path.exists(LOG_DIR): os.makedirs(LOG_DIR)

def record_strike(status, result_key, mode):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] MODE: {mode} | STATUS: {status} | BAL: {result_key}\n")

# --- 2. THE COMMAND BRIDGE ---
class LuminaZeroPoint(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🜏 LUMINA: ZERO-POINT FORGE V. 9.0")
        self.geometry("1000x800")
        self.configure(bg="#050505")
        
        self.f = tk.Frame(self, bg="#050505", padx=20, pady=20)
        self.f.pack(fill=tk.BOTH, expand=True)

        # 1. HEADER
        tk.Label(self.f, text="🜏 LUMINA ZERO-POINT: 1 - 1 = 0 🜏", 
                 bg="#050505", fg="#00ff41", font=("Courier", 20, "bold")).pack(side=tk.TOP, pady=(0, 10))
        
        self.stats_label = tk.Label(self.f, text="📊 [SYSTEM]: BALANCED STANDBY", 
                                   bg="#050505", fg="#008f11", font=("Courier", 10))
        self.stats_label.pack(side=tk.TOP, pady=5)

        # 2. INPUT AREA (VARIABLE COUNT)
        tk.Label(self.f, text="[CHAOS FIELD SIZE (VARS)]:", bg="#050505", fg="#00ff41", font=("Courier", 10)).pack(side=tk.TOP, anchor="w")
        self.v_entry = tk.Entry(self.f, bg="#111", fg="#00ff41", insertbackground="#00ff41", font=("Courier", 14), borderwidth=0)
        self.v_entry.pack(side=tk.TOP, fill=tk.X, pady=10)
        self.v_entry.insert(0, "100")

        # 3. ACTION BUTTON
        self.strike_btn = tk.Button(self.f, text="SEEK EQUILIBRIUM (STRIKE)", bg="#00ff41", fg="#000", 
                                   activebackground="#008f11", font=("Courier", 12, "bold"), 
                                   command=self.launch_strike, relief=tk.FLAT, pady=10)
        self.strike_btn.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        # 4. TERMINAL
        self.terminal = scrolledtext.ScrolledText(self.f, bg="#000", fg="#00ff41", 
                                                 font=("Courier", 11), borderwidth=0,
                                                 highlightthickness=1, highlightbackground="#333")
        self.terminal.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=10)

    def log(self, msg): 
        self.after(0, lambda: self.terminal.insert(tk.END, f"> {msg}\n") or self.terminal.see(tk.END))

    def launch_strike(self):
        self.strike_btn.config(state=tk.DISABLED, bg="#222")
        threading.Thread(target=self.maceration, daemon=True).start()

    def maceration(self):
        try:
            num_vars = int(self.v_entry.get().strip())
            self.log(f"🌌 [RITUAL]: Generating Chaos Field with {num_vars} variables...")
            
            # Generate Random 3-SAT Chaos
            clauses = []
            for _ in range(num_vars * 3): # Clause-to-Variable ratio
                c = [random.choice([1, -1]) * random.randint(1, num_vars) for _ in range(3)]
                clauses.append(c)
            
            # Hand ownership to Rust Vault
            forge = titan_forge.Forge(clauses, num_vars)
            
            self.log("⚖️ [SHAPE]: Calibrating 1 - 1 = 0 Balance Manifold...")
            # Note: This requires the inject_zero_point_balance method in your Rust lib.rs
            # If you haven't recompiled Rust yet, it will use standard search.
            if hasattr(forge, 'inject_zero_point_balance'):
                forge.inject_zero_point_balance()
            
            start = time.time()
            self.log("🔥 [STRIKE]: Hunting for the Zero-Point...")
            
            result = forge.solve_internal()
            dur = time.time() - start
            
            if result:
                pos = sum(1 for x in result if x > 0)
                neg = sum(1 for x in result if x < 0)
                balance_key = f"+{pos}/-{neg}"
                self.log(f"💎 [RESONANCE]: Harmony Found in {dur:.4f}s.")
                self.log(f"⚖️ [EQUILIBRIUM]: {balance_key}")
                record_strike("SUCCESS", balance_key, "ZERO_POINT")
            else:
                self.log("❌ [CONFLICT]: Absolute Chaos detected. No Harmony found.")
                record_strike("FAILED", "NONE", "ZERO_POINT")
                    
        except Exception as e:
            self.log(f"⚠️ [GHOST]: Error in the machine - {e}")

        self.after(0, lambda: self.strike_btn.config(state=tk.NORMAL, bg="#00ff41"))

if __name__ == "__main__":
    app = LuminaZeroPoint()
    app.mainloop()
