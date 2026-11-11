def max_element(l: list):
    if not l:
        raise ValueError("The list is empty")
    
    max_value = l[0]
    for num in l:
        if num > max_value:
            max_value = num
    return max_value