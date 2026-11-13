import sys

def min_performance_duration(a, b, c, d):
    max_diff = max(abs(a - b), abs(b - c), abs(c - a))
    return (max_diff + d - 1) // d

if __name__ == "__main__":
    input = sys.stdin.read
    data = list(map(int, input().split()))
    a, b, c, d = data[0], data[1], data[2], data[3]
    result = min_performance_duration(a, b, c, d)
    print(result)