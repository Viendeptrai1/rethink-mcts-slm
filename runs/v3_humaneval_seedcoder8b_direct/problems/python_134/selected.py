def check_if_last_char_is_a_letter(txt):
    if not txt:
        return False
    
    last_char = txt[-1]
    if not last_char.isalpha():
        return False
    
    words = txt.split()
    if not words:
        return False
    
    last_word = words[-1]
    return last_char == last_word[-1]