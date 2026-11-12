def max_pieces(n, a, b):
    total_pieces = a + b
    min_pieces_per_plate = total_pieces // n
    while True:
        if (a >= min_pieces_per_plate and b >= min_pieces_per_plate):
            return min_pieces_per_plate
        min_pieces_per_plate -= 1

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
a = int(data[1])
b = int(data[2])
print(max_pieces(n, a, b))