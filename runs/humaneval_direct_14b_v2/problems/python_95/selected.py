def check_dict_case(d):
    if not d:
        return False
    
    all_lower = all(isinstance(k, str) and k.islower() for k in d.keys())
    all_upper = all(isinstance(k, str) and k.isupper() for k in d.keys())
    
    return all_lower or all_upper