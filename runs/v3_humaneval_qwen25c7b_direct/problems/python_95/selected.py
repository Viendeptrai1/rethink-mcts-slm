def check_dict_case(dct):
    if not dct:
        return False

    has_lower = any(key.islower() for key in dct)
    has_upper = any(key.isupper() for key in dct)

    return has_lower != has_upper