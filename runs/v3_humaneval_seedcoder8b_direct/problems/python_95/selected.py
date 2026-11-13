def check_dict_case(dict):
    if not dict:
        return False
    
    lower_keys = all(isinstance(k, str) and k.islower() for k in dict.keys())
    upper_keys = all(isinstance(k, str) and k.isupper() for k in dict.keys())
    
    return lower_keys or upper_keys