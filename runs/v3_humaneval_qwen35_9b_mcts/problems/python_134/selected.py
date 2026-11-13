def check_if_last_char_is_a_letter(txt):
    if not txt:
        return False
    
    last_char = txt[-1]
    
    if not last_char.isalpha():
        return False
    
    if len(txt) == 1:
        return True
    
    if txt[-2] == ' ':
        return True
    
    return False