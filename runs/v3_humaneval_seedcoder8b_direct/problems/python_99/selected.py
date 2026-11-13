def closest_integer(value):
    num = float(value)
    lower = int(num)
    upper = lower + 1
    
    if num - lower >= 0.5 or (num - lower == 0.5 and num > 0):
        return upper
    else:
        return lower