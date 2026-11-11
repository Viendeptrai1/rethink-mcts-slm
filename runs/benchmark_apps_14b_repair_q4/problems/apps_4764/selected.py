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
input = sys.stdin.read
data = input().split()

# Convert input values to integers
n = int(data[0])
h = int(data[1])
v = int(data[2])

# Calculate and print the volume of the largest piece
print(largest_piece_volume(n, h, v))