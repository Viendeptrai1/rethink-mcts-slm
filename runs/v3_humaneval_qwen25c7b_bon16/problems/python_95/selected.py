def check_dict_case(dictionary):
    if not dictionary:
        return False

    keys = list(dictionary.keys())
    if all(key.islower() for key in keys):
        return True
    elif all(key.isupper() for key in keys):
        return True
    else:
        return False