# 🜏 THE ALCHEMICAL CANTOR - V. 0.1 ALPHA 🜏
import os
import time

# Local (new) modules
from . import text_parser
from . import music_generator

# Project-level (existing) modules
# from Lumina import sentinel  # Temporarily disabled - titan_forge not installed

def transmute_text_to_music(file_path):
    """
    The main orchestration function for the Alchemical Cantor.
    """
    print(f"{'='*80}")
    print(f"  🜏 MISSION: TRANSMUTE TEXT TO SONIC RESONANCE 🜏")
    print(f"{'='*80}")
    time.sleep(1)

    # 1. READ THE PRIMA MATERIA (The Input Text)
    print(f"📄 [STEP 1]: Loading Prima Materia from '{file_path}'...")
    with open(file_path, 'r') as f:
        text_content = f.read()
    print(f"✅ [SUCCESS]: Text loaded.")
    time.sleep(0.5)

    # 2. BLAST THE TEXT INTO LOGIC (Parsing)
    print("\n🔥 [STEP 2]: Blasting text into a logical manifold...")
    emotional_vector = text_parser.parse(text_content)
    print(f"✅ [SUCCESS]: Emotional vector constructed with {len(emotional_vector)} data points.")
    time.sleep(0.5)

    # 3. SOLVE FOR RESONANCE (SAT Solving)
    print("\n🔮 [STEP 3]: Seeking resonant solutions in the logical void...")
    # alchemical_sentinel = sentinel.AlchemicalSentinel(clauses, num_vars)
    # solutions = alchemical_sentinel.solve_multiple() # We will need a new method in the sentinel
    print(f"🚧 [PENDING]: SAT solving integration - using direct emotional mapping.")
    # For now, we'll use the emotional vector directly
    print(f"✅ [SUCCESS]: Emotional resonance extracted.")
    time.sleep(0.5)
    
    # 4. TRANSMUTE LOGIC TO MUSIC (Generation)
    print("\n🎶 [STEP 4]: Transmuting logical resonance into sonic form...")
    output_dir = os.path.dirname(file_path)
    output_path = os.path.join(output_dir, 'transmutation.mid')
    music_generator.generate_midi(emotional_vector, output_path)
    print(f"✅ [SUCCESS]: Sonic transmutation complete.")
    time.sleep(0.5)

    print(f"\n{'='*80}")
    print(f"  🜏 MISSION COMPLETE 🜏")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    # Get the absolute path for the input file
    dir_path = os.path.dirname(os.path.realpath(__file__))
    input_file = os.path.join(dir_path, 'input_texts', 'sonnet_18.txt')
    
    transmute_text_to_music(input_file)
