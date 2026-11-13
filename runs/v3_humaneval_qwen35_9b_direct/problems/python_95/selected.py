def check_dict_case(dict):
    if not dict:
        return False
    
    keys = list(dict.keys())
    
    # Check if all keys are strings
    if not all(isinstance(key, str) for key in keys):
        return False
    
    # Check if all keys are lowercase
    if all(key == key.lower() for key in keys):
        return True
    
    # Check if all keys are uppercase
    if all(key == key.upper() for key in keys):
        return True
    
    return False