def check_dict_case(dict):
    if not dict:
        return False
    
    lower_case = upper_case = True
    
    for key in dict.keys():
        if not isinstance(key, str):
            return False
        if key.islower():
            upper_case = False
        elif key.isupper():
            lower_case = False
        else:
            return False
        
        if not lower_case and not upper_case:
            return False
    
    return True