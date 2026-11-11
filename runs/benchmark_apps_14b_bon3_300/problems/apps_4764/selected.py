def largest_piece_volume(n, h, v):
    # Calculate the areas of the four pieces
    piece1 = h * v
    piece2 = h * (n - v)
    piece3 = (n - h) * v
    piece4 = (n - h) * (n - v)
    
    # Find the maximum area
    max_area = max(piece1, piece2, piece3, piece4)
    
    # Each cake is 4 cm thick
    thickness = 4
    
    # Calculate the volume of the largest piece
    max_volume = max_area * thickness
    
    return max_volume

# Read input from stdin
import sys
input = sys.stdin.read().strip().split()
n = int(input[0])
h = int(input[1])
v = int(input[2])

# Print the result
print(largest_piece_volume(n, h, v))