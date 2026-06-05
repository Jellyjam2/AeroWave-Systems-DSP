import titan_forge
import time

class AlchemicalSentinel:
    def __init__(self, clauses, num_vars):
        self.num_vars = num_vars
        self.clauses = clauses
        self.assignment = {}
        try:
            self.vault = titan_forge.Forge(self.clauses, self.num_vars)
        except Exception as e:
            print(f"❌ [CRITICAL]: Forge Conflict - {e}")
            self.vault = None

    def solve(self):
        if not self.vault: return False
        result_model = self.vault.solve_internal()
        if result_model:
            self.assignment = {abs(lit): (lit > 0) for lit in result_model}
            return True
        return False
