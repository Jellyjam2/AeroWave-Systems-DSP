# 🜏 LUMINA: ZERO-POINT FORGE V. 9.2 - TERRYOLOGY EDITION 🜏
import tkinter as tk
from tkinter import scrolledtext
import threading
import time
import random
import titan_forge 

class LuminaZeroPoint(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🜏 LUMINA: ZERO-POINT FORGE")
        self.geometry("1000x800")
        self.configure(bg="#050505")
        
        self.f = tk.Frame(self, bg="#050505", padx=20, pady=20)
        self.f.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.f, text="🜏 LUMINA ZERO-POINT: 1 - 1 = 0 🜏", 
                 bg="#050505", fg="#00ff41", font=("Courier", 20, "bold")).pack(pady=(0, 10))
        
        # INPUT: Chaos Field Size
        tk.Label(self.f, text="[CHAOS FIELD SIZE (VARS)]:", bg="#050505", fg="#00ff41", font=("Courier", 10)).pack(anchor="w")
        self.v_entry = tk.Entry(self.f, bg="#111", fg="#00ff41", font=("Courier", 14), borderwidth=0)
        self.v_entry.pack(fill=tk.X, pady=10)
        self.v_entry.insert(0, "100")

        self.terminal = scrolledtext.ScrolledText(self.f, bg="#000", fg="#00ff41", font=("Courier", 11), borderwidth=0)
        self.terminal.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.strike_btn = tk.Button(self.f, text="EXECUTE EQUILIBRIUM STRIKE", bg="#00ff41", fg="#000", 
                                   font=("Courier", 12, "bold"), command=self.launch_strike, relief=tk.FLAT, pady=10)
        self.strike_btn.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

    def log(self, msg): 
        self.after(0, lambda: self.terminal.insert(tk.END, f"> {msg}\n") or self.terminal.see(tk.END))

    def launch_strike(self):
        self.strike_btn.config(state=tk.DISABLED, bg="#222")
        threading.Thread(target=self.maceration, daemon=True).start()

    def maceration(self):
        try:
            num_vars = int(self.v_entry.get().strip())
            self.log(f"🌌 [RITUAL]: Generating Chaos Field ({num_vars} vars)...")
            
            # Generate 3-SAT Chaos (3 clauses per variable)
            clauses = [[random.choice([1, -1]) * random.randint(1, num_vars) for _ in range(3)] for _ in range(num_vars * 3)]
            
            forge = titan_forge.Forge(clauses, num_vars)
            
            start = time.time()
            self.log("🔥 [STRIKE]: Seeking Zero-Point Harmony...")
            
            result = forge.solve_internal()
            dur = time.time() - start
            
            if result:
                # Use Rust to calculate the Equilibrium report
                pos, neg, dist = forge.get_equilibrium_report(result)
                
                self.log(f"✅ [RESONANCE]: Strike complete in {dur:.4f}s.")
                self.log(f"⚖️ [REPORT]: Pos: {pos} | Neg: {neg}")
                self.log(f"📏 [HOWARD DISTANCE]: {dist}")
                
                if dist == 0:
                    self.log("💎 [ZERO-POINT]: Absolute Equilibrium Achieved. 1 - 1 = 0")
                else:
                    self.log(f"⚠️ [DRIFT]: Polarity bias detected. 1 - 1 = {dist}")
            else:
                self.log("❌ [CONFLICT]: The Chaos is absolute. No Harmony found.")
                    
        except Exception as e:
            self.log(f"⚠️ [GHOST]: Error - {e}")
        self.after(0, lambda: self.strike_btn.config(state=tk.NORMAL, bg="#00ff41"))

if __name__ == "__main__":
    LuminaZeroPoint().mainloop()
