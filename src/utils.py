import json

def load_banned_words():
    with open('config/banned_words.json', 'r') as f:
        data = json.load(f)
    return data['banned_words']

banned_words = load_banned_words()

def contains_banned_words(text):
    """
    Check if a text contains any banned words.

    Args:
        text (str): Text to be checked for banned words.
    Returns:
        bool: True if the text contains banned words, False otherwise.
       
    """
    for word in banned_words:
        if word in text.lower():
            return True
    return False