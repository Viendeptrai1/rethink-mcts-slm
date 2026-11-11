def check_if_last_char_is_a_letter(txt):
    # Trim any trailing whitespace from the string
    txt = txt.rstrip()
    
    # Split the string into words
    words = txt.split()
    
    # Check if the last word is a single alphabetical character
    if words and len(words[-1]) == 1 and words[-1].isalpha():
        return True
    else:
        return False