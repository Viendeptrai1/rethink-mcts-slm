import math

def triangle_area(a, b, c):
    if a + b > c and b + c > a and a + c > b:
        s = (a + b + c) / 2
        area = math.sqrt(s * (s - a) * (s - b) * (s - c))
        return round(area, 2)
    else:
        return -1