def check_dict_case(dct):
    if not dct:
        return False

    keys = list(dct.keys())
    if not all(isinstance(key, str) for key in keys):
        return False

    lower_case = all(key.islower() for key in keys)
    upper_case = all(key.isupper() for key in keys)

    return lower_case or upper_case