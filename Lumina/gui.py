import tkinter as tk
from tkinter import ttk, scrolledtext
import time
import threading

class LuminaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🜏 LUMINA: SOVEREIGN INTERFACE")
        self.root.geometry("900x750")
        self.root.configure(bg="#050505")

        self.main_frame = tk.Frame(self.root, bg="#050505", padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # 1. HEADER
        tk.Label(self.main_frame, text="🜏 LUMINA: THE MASTER KEY - TITAN RANK V. 1.8 🜏", 
                 bg="#050505", fg="#00ff41", font=("Courier", 18, "bold")).pack(pady=(0, 20))

        # 2. MISSION SELECTOR
        tk.Label(self.main_frame, text="[SELECT MISSION MODE]:", bg="#050505", fg="#00ff41", font=("Courier", 10)).pack(anchor="w")
        self.mode_var = tk.StringVar(value="VOYNICH DECRYPTION")
        self.mode_menu = ttk.Combobox(self.main_frame, textvariable=self.mode_var, 
                                     values=["VOYNICH DECRYPTION", "SOVEREIGN SUDOKU"], state="readonly")
        self.mode_menu.pack(fill=tk.X, pady=(0, 10))

        # 3. THE PHYSICAL PORTAL
        tk.Label(self.main_frame, text="[MISSION DATA INPUT (GLYPHS OR 81-DIGIT GRID)]:", 
                 bg="#050505", fg="#00ff41", font=("Courier", 10)).pack(anchor="w")
        self.glyph_entry = tk.Entry(self.main_frame, bg="#111", fg="#00ff41", insertbackground="#00ff41", 
                                   font=("Courier", 14), borderwidth=0, highlightthickness=1, highlightbackground="#333")
        self.glyph_entry.pack(fill=tk.X, pady=5)
        self.glyph_entry.insert(0, "daiin-8am-alkua")

        # 4. VIVIFICATION GAUGE
        tk.Label(self.main_frame, text="[VIVIFICATION GAUGE]:", bg="#050505", fg="#00ff41", font=("Courier", 10)).pack(anchor="w", pady=(10, 0))
        self.gauge = ttk.Progressbar(self.main_frame, orient=tk.HORIZONTAL, length=100, mode='determinate')
        self.gauge.pack(fill=tk.X, pady=5)

        # 5. DECRYPTION TERMINAL
        self.terminal = scrolledtext.ScrolledText(self.main_frame, bg="#000", fg="#00ff41", 
                                                 font=("Courier", 10), borderwidth=0, 
                                                 highlightthickness=1, highlightbackground="#333")
        self.terminal.pack(fill=tk.BOTH, expand=True, pady=10)

        # 6. ACTION BUTTONS
        self.strike_btn = tk.Button(self.main_frame, text="EXECUTE MISSION", bg="#00ff41", fg="#000", 
                                   activebackground="#008f11", font=("Courier", 11, "bold"), 
                                   relief=tk.FLAT, padx=20, command=self.start_decryption)
        self.strike_btn.pack(side=tk.RIGHT)

        self.clear_btn = tk.Button(self.main_frame, text="CLEAR PORTAL", bg="#333", fg="#00ff41", 
                                  activebackground="#444", font=("Courier", 11), 
                                  relief=tk.FLAT, padx=20, command=self.clear_portal)
        self.clear_btn.pack(side=tk.RIGHT, padx=10)

    def log(self, message):
        self.terminal.insert(tk.END, f"> {message}\n")
        self.terminal.see(tk.END)

    def clear_portal(self):
        """Perform a full Stibium Purge of the interface and logic."""
        self.glyph_entry.delete(0, tk.END)
        self.terminal.delete('1.0', tk.END)
        self.gauge['value'] = 0
        self.log("🜏 PORTAL CLEARED. ALL GLYPHS EXPUNGED.")
        # If the sentinel exists in the master execution, reset its mineral weights
        if hasattr(self, 'sentinel') and self.sentinel:
            self.sentinel.catalysts = {v: 1.0 for v in range(1, self.sentinel.num_vars + 1)}
            self.log("⚖️ [STIBIUM PURGE]: MINERAL WEIGHTS RESET TO 1.0.")

    def start_decryption(self):
        self.strike_btn.config(state=tk.DISABLED, bg="#333")
        threading.Thread(target=self.macerate_sequence, daemon=True).start()

    def macerate_sequence(self):
        """This logic is overridden by MasterKeyGUI in main.py"""
        self.log("📡 STANDING BY FOR MASTER KEY INSTRUCTIONS...")
        time.sleep(1)
        self.strike_btn.config(state=tk.NORMAL, bg="#00ff41")

if __name__ == "__main__":
    root = tk.Tk()
    app = LuminaGUI(root)
    root.mainloop()
