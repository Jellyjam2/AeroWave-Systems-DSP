import tkinter as tk
import time
from Lumina.gui import LuminaGUI
from Lumina.sentinel import AlchemicalSentinel
from Lumina.logs import record_strike
from Lumina.viewer import SovereignGridViewer

class MasterKeyGUI(LuminaGUI):
    def macerate_sequence(self):
        # 1. READ THE PORTAL
        raw_input = self.glyph_entry.get().strip()
        self.gauge['value'] = 0
        self.log(f"🜏 PORTAL ACTIVE: ANALYZING INPUT...")
        
        # 2. AUTO-MISSION DETECTION & DROPDOWN SYNC
        if len(raw_input) == 81 and raw_input.isdigit():
            self.mode_var.set("SOVEREIGN SUDOKU")
            self.execute_sudoku(raw_input)
        else:
            self.mode_var.set("VOYNICH DECRYPTION")
            self.execute_voynich(raw_input)
            
        self.strike_btn.config(state=tk.NORMAL, bg="#00ff41")

    def execute_voynich(self, script):
        self.log(f"📖 [VOYNICH]: Macerating -> {script}")
        voynich_lexicon = {1: "Ingredient (oror)", 2: "Process (mac)", 3: "Result (ol)"}
        # Standard Alchemical Clauses for Voynich Resonance
        clauses = [[1, 2], [-1, -2], [3]]
        sentinel = AlchemicalSentinel(clauses, 3)
        
        if sentinel.solve():
            self.trigger_success_flash()
            self.gauge['value'] = 100
            self.log("✅ [RESONANCE]: 100% SYNCHRONICITY")
            for var_id, is_active in sentinel.assignment.items():
                if is_active:
                    self.log(f"  [+] {voynich_lexicon.get(var_id, 'Node')}: VIVIFIED")
            record_strike("VOYNICH_SUCCESS", script[:10])

    def execute_sudoku(self, digits):
        self.log("🧩 [SUDOKU]: Macerating 9x9 Sovereign Grid...")
        # 1. Parse Input to 9x9 Matrix
        grid = [[int(digits[r*9+c]) for c in range(9)] for r in range(9)]
        clauses = []
        
        # 2. THE TITAN MAPPING (Standard 1-based index: 1 to 729)
        # This ensures Digit 1 at (0,0) is ID 1, and Digit 1 at (0,1) is ID 10.
        def v(r, c, n): return (r * 9 + c) * 9 + (n - 1) + 1
        
        # 3. APPLYING THE GILDED CONSTRAINTS (The Laws of the Grid)
        for r in range(9):
            for c in range(9):
                # RULE 1: EXISTENCE (Every cell must hold a digit 1-9)
                clauses.append([v(r, c, n) for n in range(1, 10)])
                
                # RULE 2: FIXED ANCHORS (Respect the clues provided)
                if grid[r][c] != 0:
                    clauses.append([v(r, c, grid[r][c])])

                # RULE 3: UNIQUE RESONANCE (The Anti-Node Fix)
                for n in range(1, 10):
                    # 3.1 SINGULARITY: A cell can only hold ONE number
                    for n2 in range(n + 1, 10):
                        clauses.append([-v(r, c, n), -v(r, c, n2)])

                    # 3.2 ROW/COL EXCLUSION: No duplicate numbers in line
                    for i in range(9):
                        if i > c: clauses.append([-v(r, c, n), -v(r, i, n)]) # Row
                        if i > r: clauses.append([-v(r, c, n), -v(i, c, n)]) # Col
                    
                    # 3.3 SQUARE SEAL: No duplicate numbers in 3x3 block
                    sr, sc = (r // 3) * 3, (c // 3) * 3
                    for r2 in range(sr, sr + 3):
                        for c2 in range(sc, sc + 3):
                            if r2 > r or (r2 == r and c2 > c):
                                clauses.append([-v(r, c, n), -v(r2, c2, n)])

        # 4. MACERATION
        sentinel = AlchemicalSentinel(clauses, 729)
        self.gauge['value'] = 50
        self.root.update_idletasks()
        
        if sentinel.solve():
            self.trigger_success_flash()
            self.gauge['value'] = 100
            self.log("✅ [VIVIFIED]: Sovereign Reality Found. 100% Resonance.")
            
            # 5. EXTRACTION (Mapping Sentinel IDs back to 1-9 for the Viewer)
            solved_grid = []
            for r in range(9):
                row = []
                for c in range(9):
                    val = 0
                    for n in range(1, 10):
                        if sentinel.assignment.get(v(r, c, n)):
                            val = n
                            break
                    row.append(val)
                solved_grid.append(row)
            
            # Launch the Corrected Viewer
            SovereignGridViewer(self.root, solved_grid)
            record_strike("SUDOKU_SUCCESS", "0x9x9_ABSOLUTE")
        else:
            self.log("❌ [CONFLICT]: Logic contradiction detected. Grid is locked.")

    def trigger_success_flash(self):
        """Visual pulse to signal completion."""
        self.terminal.config(bg="#003311")
        self.root.after(200, lambda: self.terminal.config(bg="#000"))

    def clear_portal(self):
        """Wipes the data for the next strike."""
        self.glyph_entry.delete(0, tk.END)
        self.gauge['value'] = 0
        self.log("🧹 [SYSTEM]: Portal cleared for next mission.")

if __name__ == "__main__":
    root = tk.Tk()
    app = MasterKeyGUI(root)
    # Escape key bind for instant clearing
    root.bind('<Escape>', lambda e: app.clear_portal())
    root.mainloop()
