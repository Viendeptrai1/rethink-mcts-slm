import math

def truncate_number(number: float) -> float:
    return math.modf(number)[0]