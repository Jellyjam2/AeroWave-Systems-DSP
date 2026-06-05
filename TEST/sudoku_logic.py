def generate_sudoku_clauses(grid):
    clauses = []
    # 1. Map (row, col, val) to a unique variable ID (1 to 729)
    def v(r, c, n): return (r * 81) + (c * 9) + n
    
    # Rule A: Each cell must contain at least one number
    for r in range(9):
        for c in range(9):
            clauses.append([v(r, c, n) for n in range(1, 10)])
            
    # Rule B: Each number appears only once per row
    for r in range(9):
        for n in range(1, 10):
            for c1 in range(9):
                for c2 in range(c1 + 1, 9):
                    clauses.append([-v(r, c1, n), -v(r, c2, n)])
                    
    # Rule C: Each number appears only once per column
    for c in range(9):
        for n in range(1, 10):
            for r1 in range(9):
                for r2 in range(r1 + 1, 9):
                    clauses.append([-v(r1, c, n), -v(r2, c, n)])

    # Rule D: Each number appears once per 3x3 sub-grid
    for i in range(3):
        for j in range(3):
            for n in range(1, 10):
                cells = []
                for r in range(i*3, (i+1)*3):
                    for c in range(j*3, (j+1)*3):
                        cells.append(v(r, c, n))
                for k1 in range(9):
                    for k2 in range(k1 + 1, 9):
                        clauses.append([-cells[k1], -cells[k2]])

    # Rule E: Pre-filled cells (The 'Clues')
    for r in range(9):
        for c in range(9):
            if grid[r][c] != 0:
                clauses.append([v(r, c, grid[r][c])])
                
    return clauses, 729
