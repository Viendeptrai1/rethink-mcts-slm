from itertools import combinations
import math

def max_polygon_area(n, lengths):
    def is_valid_triangle(a, b, c):
        return a + b > c and a + c > b and b + c > a

    def herons_formula(a, b, c):
        s = (a + b + c) / 2
        return math.sqrt(s * (s - a) * (s - b) * (s - c))

    max_area = 0
    for r in range(3, n + 1):
        for combo in combinations(lengths, r):
            a, b, c = sorted(combo)
            if is_valid_triangle(a, b, c):
                area = herons_formula(a, b, c)
                if area > max_area:
                    max_area = area
    return max_area

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    lengths = list(map(int, data[1:]))
    result = max_polygon_area(n, lengths)
    print(f"{result:.5f}")