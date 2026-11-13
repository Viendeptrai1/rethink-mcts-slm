def circular_shift(x, shift):
    s = str(x)
    n = len(s)
    shift = shift % n
    return s[-shift:] + s[:-shift]