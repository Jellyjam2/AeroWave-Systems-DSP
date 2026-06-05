import tkinter as tk
from tkinter import scrolledtext
import threading
import time
import os
import datetime
from pysat.solvers import Cadical153 as Solver

# --- 1. ARCHIVAL ENGINE ---
LOG_DIR = "Logs"
LOG_FILE = os.path.join(LOG_DIR, "strike_history.log")
if not os.path.exists(LOG_DIR): os.makedirs(LOG_DIR)

def record_strike(status, result_key):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] STATUS: {status} | KEY: {result_key}\n")

# --- 2. SOVEREIGN SUDOKU LOGIC ---
def generate_sudoku_clauses(grid_string):
    """The 15th-Century Lexicon of Logic Gates."""
    def v(r, c, n): return (r * 81) + (c * 9) + n
    clauses = []
    
    # Rule A: One number per cell
    for r in range(9):
        for c in range(9):
            clauses.append([v(r, c, n) for n in range(1, 10)])
            for n1 in range(1, 10):
                for n2 in range(n1 + 1, 10):
                    clauses.append([-v(r, c, n1), -v(r, c, n2)])
    
    # Rule B: Row/Column Uniqueness
    for n in range(1, 10):
        for i in range(9):
            clauses.append([v(i, j, n) for j in range(9)]) # Row
            clauses.append([v(j, i, n) for j in range(9)]) # Col
            for j1 in range(9):
                for j2 in range(j1 + 1, 9):
                    clauses.append([-v(i, j1, n), -v(i, j2, n)])
                    clauses.append([-v(j1, i, n), -v(j2, i, n)])

    # Rule C: 3x3 Sub-grid Constraints
    for r_off in [0, 3, 6]:
        for c_off in [0, 3, 6]:
            for n in range(1, 10):
                box = [v(r_off + r, c_off + c, n) for r in range(3) for c in range(3)]
                clauses.append(box)
                for i in range(9):
                    for j in range(i + 1, 9):
                        clauses.append([-box[i], -box[j]])

    # Rule D: Inject Clues from Portal
    grid_string = grid_string.replace(".", "0").replace(" ", "").strip()
    for i, char in enumerate(grid_string):
        if char != "0":
            row, col = divmod(i, 9)
            clauses.append([v(row, col, int(char))])
            
    return clauses

# --- 3. THE COMMAND BRIDGE ---
class LuminaRedPill(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🜏 LUMINA: RED PILL V. 5.2 🜏")
        self.geometry("1000x800")
        self.configure(bg="#050505")
        
        f = tk.Frame(self, bg="#050505", padx=20, pady=20); f.pack(fill=tk.BOTH, expand=True)
        
        # HEADER
        tk.Label(f, text="🜏 LUMINA RED PILL: VIVIFIED CORE 🜏", 
                 bg="#050505", fg="#00ff41", font=("Courier", 22, "bold")).pack()
        
        self.stats_label = tk.Label(f, text="📊 [SYSTEM]: STANDING BY", 
                                   bg="#050505", fg="#008f11", font=("Courier", 10))
        self.stats_label.pack(pady=5)

        # MISSION PORTAL
        tk.Label(f, text="[PORTAL INPUT - 81 GLYPHS]:", bg="#050505", fg="#00ff41", font=("Courier", 10)).pack(anchor="w")
        self.glyph_entry = tk.Entry(f, bg="#111", fg="#00ff41", insertbackground="#00ff41", 
                                   font=("Courier", 14), borderwidth=0, highlightthickness=1, highlightbackground="#333")
        self.glyph_entry.pack(fill=tk.X, pady=10)
        # Pre-load AI Escargot
        self.glyph_entry.insert(0, "1....7.9..3..2...8..96..5....53..9...1..8...26....4...3......1..4......7..7...3..")

        # TERMINAL
        self.terminal = scrolledtext.ScrolledText(f, bg="#000", fg="#00ff41", 
                                                 font=("Courier", 11), borderwidth=0, 
                                                 highlightthickness=1, highlightbackground="#333")
        self.terminal.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # CONTROL
        self.strike_btn = tk.Button(f, text="EXECUTE RITUAL STRIKE", bg="#00ff41", fg="#000", 
                                   font=("Courier", 12, "bold"), relief=tk.FLAT, padx=20,
                                   command=self.launch_strike)
        self.strike_btn.pack(side=tk.RIGHT, pady=10)
        
        self.update_dashboard()

    def log(self, msg): 
        self.after(0, lambda: self.terminal.insert(tk.END, f"> {msg}\n") or self.terminal.see(tk.END))

    def update_dashboard(self):
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f: lines = f.readlines()
            successes = sum(1 for l in lines if "SUCCESS" in l)
            self.stats_label.config(text=f"📊 SESSIONS: {len(lines)} | SUCCESS: {successes} | RAM: PROTECTED")

    def launch_strike(self):
        self.strike_btn.config(state=tk.DISABLED, bg="#222")
        threading.Thread(target=self.maceration, daemon=True).start()

    def maceration(self):
        grid_data = self.glyph_entry.get()
        self.log("📡 [STIBIUM]: Synchronizing 15th-Century Lexicon...")
        time.sleep(0.4)
        
        try:
            # 1. GENERATE GATES
            clauses = generate_sudoku_clauses(grid_data)
            self.log(f"⚖️ [RESONANCE]: {len(clauses)} logic gates vivified.")
            
            # 2. ENGAGE ENGINE (FIXED SYNTAX)
            with Solver() as s:
                s.append_formula(clauses) # Pour the gates into the machine
                start = time.time()
                
                self.log("🔥 [MACERATION]: Piercing the grid...")
                if s.solve():
                    dur = time.time() - start
                    self.log(f"✅ [SUCCESS]: Resonance found in {dur:.4f}s")
                    record_strike("SUCCESS", "SUDOKU_GRID")
                else:
                    self.log("❌ [CONFLICT]: Thermal runaway. Vault remains sealed.")
                    record_strike("FAILED", "CONFLICT")
                    
        except Exception as e:
            self.log(f"⚠️ [GHOST]: Error in the machine - {e}")

        self.update_dashboard()
        self.after(0, lambda: self.strike_btn.config(state=tk.NORMAL, bg="#00ff41"))

if __name__ == "__main__":
    app = LuminaRedPill()
    app.mainloop()
