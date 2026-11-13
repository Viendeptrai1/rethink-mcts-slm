import math

def closest_integer(value):
    num = float(value)
    if abs(num - round(num)) == 0.5:
        return int(math.ceil(num) if num > 0 else math.floor(num))
    return round(num)