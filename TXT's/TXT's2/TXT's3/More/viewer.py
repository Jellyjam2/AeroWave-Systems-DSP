import tkinter as tk

class SovereignGridViewer:
    def __init__(self, root, grid):
        self.window = tk.Toplevel(root)
        self.window.title("🜏 LUMINA: SOVEREIGN GRID VIEWER")
        self.window.configure(bg="#050505")
        self.cells = {}
        
        # Create 9x9 Matrix
        for r in range(9):
            for c in range(9):
                # Border styling for 3x3 blocks
                padx = (5, 1) if c % 3 == 0 else 1
                pady = (5, 1) if r % 3 == 0 else 1
                
                color = "#00ff41" if grid[r][c] != 0 else "#008f11"
                val = str(grid[r][c]) if grid[r][c] != 0 else " "
                
                lbl = tk.Label(self.window, text=val, width=4, height=2,
                               bg="#111", fg=color, font=("Courier", 14, "bold"),
                               relief=tk.FLAT, highlightthickness=1, 
                               highlightbackground="#333")
                lbl.grid(row=r, column=c, padx=padx, pady=pady)
                self.cells[(r, c)] = lbl

    def update_cell(self, r, c, val):
        self.cells[(r, c)].config(text=str(val), fg="#00ff41")
