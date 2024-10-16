"""
    Module for adding utility functions to the program.
"""

import json
import os
import sys

# Function to load banned words from a json file
def load_banned_words():
    """
    Load banned words from a json file.

    Returns:
        list: A list of banned words.
    """
    with open(os.path.join(os.path.dirname(__file__), 'banned_words.json')) as f:
        banned_words = json.load(f)
    return banned_words

banned_words = load_banned_words()

def contains_banned_words(text):
    """
    Check if a text contains any banned words.

    Args:
        text (str): Text to be checked for banned words.
    Returns:
        bool: True if the text contains banned words, False otherwise.
       
    """
    for word in text.lower():
        if word in banned_words:
            return True
    return False