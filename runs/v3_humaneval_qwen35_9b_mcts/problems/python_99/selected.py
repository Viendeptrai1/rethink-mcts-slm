import math

def closest_integer(value):
    """
    Create a function that takes a value (string) representing a number
    and returns the closest integer to it. If the number is equidistant
    from two integers, round it away from zero.
    """
    num = float(value)
    floor_val = math.floor(num)
    ceil_val = math.ceil(num)
    
    if num - floor_val < ceil_val - num:
        return floor_val
    elif num - floor_val > ceil_val - num:
        return ceil_val
    else:
        # Equidistant: round away from zero
        if num > 0:
            return ceil_val
        else:
            return floor_val