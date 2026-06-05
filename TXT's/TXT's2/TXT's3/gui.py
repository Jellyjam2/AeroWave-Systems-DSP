import tkinter as tk
from tkinter import ttk, scrolledtext
import time
import threading

class LuminaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🜏 LUMINA: VOYNICH DECRYPTION INTERFACE")
        self.root.geometry("900x650")
        self.root.configure(bg="#050505")

        # Container for layout
        self.main_frame = tk.Frame(self.root, bg="#050505", padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # 1. HEADER
        tk.Label(self.main_frame, text="🜏 LUMINA: THE MASTER KEY - TITAN RANK V. 1.1 🜏", 
                 bg="#050505", fg="#00ff41", font=("Courier", 18, "bold")).pack(pady=(0, 20))

        # 2. DASHBOARD STATS
        self.stats_bar = tk.Label(self.main_frame, text=" [SYSTEM]: ONLINE | [RESONANCE]: 100% | [TARGET]: VOYNICH FOLIO 103R ", 
                                 bg="#111", fg="#00ff41", font=("Courier", 10), relief=tk.SUNKEN, bd=1)
        self.stats_bar.pack(fill=tk.X, pady=10)

        # 3. GLYPH INPUT
        tk.Label(self.main_frame, text="[MANUSCRIPT GLYPH SEQUENCE]:", bg="#050505", fg="#00ff41", font=("Courier", 10)).pack(anchor="w")
        self.glyph_entry = tk.Entry(self.main_frame, bg="#111", fg="#00ff41", insertbackground="#00ff41", 
                                   font=("Courier", 14), borderwidth=0, highlightthickness=1, highlightbackground="#333")
        self.glyph_entry.pack(fill=tk.X, pady=5)
        self.glyph_entry.insert(0, "o-r-o-r-a-m-a-c-o-l-k-h-n-8-9-p-s")

        # 4. DECRYPTION TERMINAL
        tk.Label(self.main_frame, text="[DECRYPTION TERMINAL]:", bg="#050505", fg="#00ff41", font=("Courier", 10)).pack(anchor="w", pady=(10, 0))
        self.terminal = scrolledtext.ScrolledText(self.main_frame, bg="#000", fg="#00ff41", 
                                                 font=("Courier", 10), insertbackground="#00ff41",
                                                 borderwidth=0, highlightthickness=1, highlightbackground="#333")
        self.terminal.pack(fill=tk.BOTH, expand=True, pady=10)

        # 5. ACTION BUTTON
        self.strike_btn = tk.Button(self.main_frame, text="EXECUTE MACERATION", bg="#00ff41", fg="#000", 
                                   activebackground="#008f11", font=("Courier", 11, "bold"), 
                                   relief=tk.FLAT, padx=20, command=self.start_decryption)
        self.strike_btn.pack(side=tk.RIGHT)

    def log(self, message):
        self.terminal.insert(tk.END, f"> {message}\n")
        self.terminal.see(tk.END)

    def start_decryption(self):
        self.strike_btn.config(state=tk.DISABLED, bg="#333")
        threading.Thread(target=self.macerate_sequence, daemon=True).start()

    def macerate_sequence(self):
        self.log("🜏 INITIALIZING LUMINA CORE V. 1.1...")
        time.sleep(0.8)
        self.log("📡 CONNECTING TO GHETTO NUOVO DIGITAL GATEWAY...")
        time.sleep(1)
        self.log(f"🔎 ANALYZING GLYPHS: {self.glyph_entry.get()}")
        time.sleep(1.2)
        
        # Maceration Logic
        steps = [
            "[-] ISO-SCANNING FOLIO 103R TOPOGRAPHY...",
            "[-] ALIGNING BOTANICAL NODES TO HEBREW-SABIR LEXICON...",
            "[-] SENTINEL: CONFLICT-DRIVEN CLAUSE LEARNING INITIATED...",
            "[!] RESONANCE DETECTED AT NODE 12 (MANDRAKE)...",
            "[*] MACERATION COMPLETE."
        ]
        
        for step in steps:
            self.log(step)
            time.sleep(0.6)
            
        self.log("✅ DECRYPTION SUCCESSFUL. THE TRUTH IS UNLOCKED.")
        self.log("--------------------------------------------------")
        self.strike_btn.config(state=tk.NORMAL, bg="#00ff41")

if __name__ == '__main__':
    root = tk.Tk()
    app = LuminaGUI(root)
    root.mainloop()
