import re

def parse(text_content: str) -> list[float]:
    """
    Parses the input text into a numerical "emotional vector".
    Each word is assigned a score based on its length to simulate emotional weight.

    Args:
        text_content: The raw string content of the text.

    Returns:
        A list of floats representing the emotional vector of the text.
    """
    emotional_vector = []
    
    # Normalize text: lowercase and remove punctuation
    processed_text = re.sub(r'[^\w\s]', '', text_content).lower()

    words = processed_text.split()
    
    for word in words:
        # Calculate a simple "emotional score" based on word length.
        # Longer words are given more weight.
        score = min(len(word) / 10.0, 1.0) # Normalize to a max of 1.0
        emotional_vector.append(score)

    print(f"  [PARSER]: Generated an emotional vector with {len(emotional_vector)} data points.")

    return emotional_vector

