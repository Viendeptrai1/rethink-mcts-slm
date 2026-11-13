import math

def max_sheep_pen_area(segments):
    n = len(segments)
    segments.sort(reverse=True)
    
    def is_triangle(a, b, c):
        return a + b > c and b + c > a and c + a > b
    
    def triangle_area(a, b, c):
        s = (a + b + c) / 2
        return math.sqrt(s * (s - a) * (s - b) * (s - c))
    
    max_area = 0
    for i in range(n - 2):
        for j in range(i + 1, n - 1):
            for k in range(j + 1, n):
                if is_triangle(segments[i], segments[j], segments[k]):
                    area = triangle_area(segments[i], segments[j], segments[k])
                    max_area = max(max_area, area)
                    break
    
    return round(max_area, 3)

n, *segments = map(int, input().split())
result = max_sheep_pen_area(segments)
print(result)