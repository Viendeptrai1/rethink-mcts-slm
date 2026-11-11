def check_dict_case(d):
    if not d:
        return False
    
    keys = d.keys()
    
    if not all(isinstance(k, str) for k in keys):
        return False
    
    lower_case = all(k.islower() for k in keys)
    upper_case = all(k.isupper() for k in keys)
    
    return lower_case or upper_case