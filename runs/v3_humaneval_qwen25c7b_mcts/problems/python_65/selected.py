def circular_shift(x, shift):
    num_str = str(x)
    length = len(num_str)
    
    if shift == length:
        return num_str
    
    shift %= length
    return num_str[-shift:] + num_str[:-shift]