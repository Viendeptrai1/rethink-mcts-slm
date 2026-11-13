def check_if_last_char_is_a_letter(txt):
    if not txt:
        return False
    
    last_char = txt[-1]
    
    if not last_char.isalpha():
        return False
    
    if len(txt) == 1:
        return True
    
    second_last_char = txt[-2]
    
    if second_last_char == ' ':
        return False
    
    return True