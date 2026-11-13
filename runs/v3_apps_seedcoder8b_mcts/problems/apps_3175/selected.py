import sys
import math

def max_sheep_pen_area(n, segments):
    def heron_formula(a, b, c):
        s = (a + b + c) / 2
        return math.sqrt(s * (s - a) * (s - b) * (s - c))

    def max_triangle_area(segments):
        max_area = 0
        n = len(segments)
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    a, b, c = segments[i], segments[j], segments[k]
                    if a + b > c and a + c > b and b + c > a:
                        area = heron_formula(a, b, c)
                        max_area = max(max_area, area)
        return max_area

    segments.sort(reverse=True)
    max_area = 0
    for i in range(3, n + 1):
        max_area = max(max_area, max_triangle_area(segments[:i]))
    return max_area

def main():
    input_data = sys.stdin.read().strip()
    data = list(map(int, input_data.split()))
    n = data[0]
    segments = data[1:]
    result = max_sheep_pen_area(n, segments)
    print(f"{result:.3f}")

if __name__ == "__main__":
    main()