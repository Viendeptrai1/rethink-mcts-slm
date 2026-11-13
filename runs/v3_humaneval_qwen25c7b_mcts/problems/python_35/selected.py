def max_element(l: list):
    if not l:
        return None
    max_val = l[0]
    for num in l:
        if num > max_val:
            max_val = num
    return max_val