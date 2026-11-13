import math

def truncate_number(number: float) -> float:
    fractional, integer = math.modf(number)
    return fractional