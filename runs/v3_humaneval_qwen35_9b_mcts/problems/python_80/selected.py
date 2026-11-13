def is_happy(s):
    if len(s) < 3:
        return False
    for i in range(len(s) - 2):
        triplet = s[i:i+3]
        if len(set(triplet)) != 3:
            return False
    return True