import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
import time
import threading
import os
import sys

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
        self.mode_var = tk.StringVar(value="ALCHEMICAL CANTOR")
        self.mode_menu = ttk.Combobox(self.main_frame, textvariable=self.mode_var, 
                                     values=["ALCHEMICAL CANTOR", "VOYNICH DECRYPTION", "SOVEREIGN SUDOKU"], state="readonly")
        self.mode_menu.pack(fill=tk.X, pady=(0, 10))
        self.mode_menu.bind("<<ComboboxSelected>>", self.on_mode_change)

        # 3. THE PHYSICAL PORTAL
        self.portal_label = tk.Label(self.main_frame, text="[MISSION DATA INPUT (GLYPHS OR 81-DIGIT GRID)]:", 
                 bg="#050505", fg="#00ff41", font=("Courier", 10)).pack(anchor="w")
        self.glyph_entry = tk.Entry(self.main_frame, bg="#111", fg="#00ff41", insertbackground="#00ff41", 
                                   font=("Courier", 14), borderwidth=0, highlightthickness=1, highlightbackground="#333")
        self.glyph_entry.pack(fill=tk.X, pady=5)
        self.glyph_entry.insert(0, "daiin-8am-alkua")
        
        # File selector for Alchemical Cantor mode
        self.file_btn = tk.Button(self.main_frame, text="📄 SELECT TEXT FILE", bg="#333", fg="#00ff41",
                                  activebackground="#444", font=("Courier", 10),
                                  relief=tk.FLAT, command=self.select_text_file)
        self.file_btn.pack(fill=tk.X, pady=5)
        self.file_btn.pack_forget()  # Hidden by default

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

    def on_mode_change(self, event):
        """Handle mission mode selection changes."""
        mode = self.mode_var.get()
        if mode == "ALCHEMICAL CANTOR":
            self.portal_label.config(text="[TEXT FILE INPUT (PRIMA MATERIA)]:")
            self.glyph_entry.pack_forget()
            self.file_btn.pack(fill=tk.X, pady=5)
            self.log("🜏 MODE: ALCHEMICAL CANTOR - TEXT TO SONIC TRANSMUTATION")
        else:
            self.portal_label.config(text="[MISSION DATA INPUT (GLYPHS OR 81-DIGIT GRID)]:")
            self.file_btn.pack_forget()
            self.glyph_entry.pack(fill=tk.X, pady=5)
            self.glyph_entry.delete(0, tk.END)
            self.glyph_entry.insert(0, "daiin-8am-alkua")
            self.log(f"🜏 MODE: {mode}")

    def select_text_file(self):
        """Open file dialog to select text file for Alchemical Cantor."""
        file_path = filedialog.askopenfilename(
            title="Select Prima Materia (Text File)",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            self.glyph_entry.delete(0, tk.END)
            self.glyph_entry.insert(0, file_path)
            self.log(f"📄 PRIMA MATERIA SELECTED: {os.path.basename(file_path)}")

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
        """Execute the selected mission mode."""
        mode = self.mode_var.get()
        
        if mode == "ALCHEMICAL CANTOR":
            self.execute_alchemical_cantor()
        else:
            self.log("📡 STANDING BY FOR MASTER KEY INSTRUCTIONS...")
            time.sleep(1)
            self.strike_btn.config(state=tk.NORMAL, bg="#00ff41")

    def execute_alchemical_cantor(self):
        """Execute the Alchemical Cantor text-to-music transmutation."""
        file_path = self.glyph_entry.get()
        
        if not file_path or not os.path.exists(file_path):
            self.log("❌ ERROR: No valid text file selected.")
            self.strike_btn.config(state=tk.NORMAL, bg="#00ff41")
            return
        
        try:
            # Import and run the Alchemical Cantor
            sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            from LuminaCantor import main as cantor_main
            
            # Redirect output to GUI
            self.log("🜏 INITIATING ALCHEMICAL TRANSMUTATION...")
            self.gauge['value'] = 25
            self.root.update()
            
            cantor_main.transmute_text_to_music(file_path)
            
            self.gauge['value'] = 100
            self.log("✅ TRANSMUTATION COMPLETE: MIDI file generated.")
            
        except Exception as e:
            self.log(f"❌ TRANSMUTATION FAILED: {str(e)}")
        
        self.strike_btn.config(state=tk.NORMAL, bg="#00ff41")

if __name__ == "__main__":
    root = tk.Tk()
    app = LuminaGUI(root)
    root.mainloop()
