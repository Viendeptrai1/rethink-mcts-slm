def min_problems_to_add(n, m, a, b):
    required_complexities = set(a)
    prepared_complexities = set(b)
    missing_complexities = required_complexities - prepared_complexities
    return len(missing_complexities)

# Example usage:
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
a = list(map(int, data[2:n+2]))
b = list(map(int, data[n+2:]))

print(min_problems_to_add(n, m, a, b))