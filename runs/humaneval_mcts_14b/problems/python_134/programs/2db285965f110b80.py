def check_if_last_char_is_a_letter(txt):
    # Trim trailing spaces
    txt = txt.rstrip()
    
    # Split the string into words
    words = txt.split()
    
    # Check if there are any words
    if not words:
        return False
    
    # Get the last word
    last_word = words[-1]
    
    # Check if the last word is a single letter
    return len(last_word) == 1 and last_word.isalpha()