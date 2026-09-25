def check_if_last_char_is_a_letter(txt):
    # Strip trailing spaces
    txt = txt.rstrip()
    
    # If the string is empty after stripping, return False
    if not txt:
        return False
    
    # Get the last character
    last_char = txt[-1]
    
    # Check if the last character is alphabetical
    if not last_char.isalpha():
        return False
    
    # Check if the last character is standalone
    # If the length is 1, it's standalone
    if len(txt) == 1:
        return True
    
    # Otherwise, check if the character before the last is a space
    return txt[-2] == ' '