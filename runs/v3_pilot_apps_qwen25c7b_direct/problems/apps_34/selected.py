def max_pieces(n, a, b):
    return min(a // (n - b), b // (n - a))

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
a = int(data[1])
b = int(data[2])

print(max_pieces(n, a, b))