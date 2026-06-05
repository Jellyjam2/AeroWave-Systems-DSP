# 🜏 SENTINEL.PY - THE STATEFUL COMMAND BRIDGE 🜏
import titan_forge
import time

class AlchemicalSentinel:
    """
    The High-Velocity Orchestrator.
    Now optimized to minimize FFI crossings and maximize Cache Locality.
    """
    def __init__(self, clauses, num_vars):
        self.num_vars = num_vars
        self.clauses = clauses
        self.assignment = {}
        
        # TIER 6: Ownership Transfer
        # We move the clauses into the Rust Vault immediately.
        # Python no longer manages the raw clause memory.
        try:
            self.vault = titan_forge.Forge(self.clauses, self.num_vars)
            print(f"⚖️ [STIBIUM]: {len(clauses)} clauses secured in the Rust Vault.")
        except Exception as e:
            print(f"❌ [CRITICAL]: Forge Initialization Failed - {e}")
            self.vault = None

    def solve(self):
        """
        The Silent Strike.
        Executes the entire search loop within the Rust environment.
        """
        if not self.vault:
            print("⚠️ [SENTINEL]: Cannot strike. Vault is uninitialized.")
            return False

        print("🔥 [MACERATION]: Internalizing search loop. Terminal silence engaged...")
        start_time = time.time()

        # ONE-TIME FFI CALL: The 'General' takes command.
        # This one call replaces the thousands of 'chatty' calls from the old version.
        result_model = self.vault.solve_internal()

        duration = time.time() - start_time

        if result_model:
            # Map the Rust vector back to a Python dictionary for the UI
            self.assignment = {abs(lit): (lit > 0) for lit in result_model}
            print(f"✅ [RESONANCE]: Strike complete. Speed: {duration:.8f}s")
            return True
        else:
            print("❌ [CONFLICT]: The Vault remains sealed. No solution found.")
            return False

    def tune_terrain(self, volume, noise_pattern):
        """
        Proxies the Zeroid Terrain check through the Vault.
        """
        if self.vault:
            return self.vault.zeroid_terrain_check(volume, noise_pattern)
        return volume

if __name__ == "__main__":
    # Test the Sovereign Sync
    test_clauses = [[1, 2], [-1, 3]]
    sentinel = AlchemicalSentinel(test_clauses, 3)
    if sentinel.solve():
        print(f"💎 [RESULT]: {sentinel.assignment}")
