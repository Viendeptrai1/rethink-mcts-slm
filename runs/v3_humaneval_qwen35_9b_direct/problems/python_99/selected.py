def closest_integer(value):
    try:
        num = float(value)
    except (ValueError, TypeError):
        raise ValueError("Input must be a string representing a valid number.")
    
    if num >= 0:
        return int(num + 0.5)
    else:
        return int(num - 0.5)