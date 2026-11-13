def check_dict_case(dict):
    """
    Given a dictionary, return True if all keys are strings in lower 
    case or all keys are strings in upper case, else return False.
    The function should return False is the given dictionary is empty.
    """
    if not dict:
        return False
    
    keys = dict.keys()
    all_lower = True
    all_upper = True
    
    for key in keys:
        if not isinstance(key, str):
            return False
        
        if key != key.lower():
            all_lower = False
        
        if key != key.upper():
            all_upper = False
    
    return all_lower or all_upper