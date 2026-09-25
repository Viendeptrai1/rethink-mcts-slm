def check_if_last_char_is_a_letter(txt):
    # Strip trailing spaces
    txt = txt.rstrip()
    
    # Split the text into words
    words = txt.split()
    
    # Check if there's at least one word
    if not words:
        return False
    
    # Get the last word
    last_word = words[-1]
    
    # Check if the last word is a single alphabetical character
    return len(last_word) == 1 and last_word.isalpha()