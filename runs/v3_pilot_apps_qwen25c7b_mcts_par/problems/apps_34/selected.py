def max_pieces(n, a, b):
    total_pieces = a + b
    if total_pieces < n:
        return -1
    min_pieces = total_pieces // n
    if (a >= min_pieces and b >= min_pieces) or (a < min_pieces and b < min_pieces):
        return min_pieces
    else:
        return min_pieces - 1

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
a = int(data[1])
b = int(data[2])
print(max_pieces(n, a, b))