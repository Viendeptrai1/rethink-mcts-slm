def largest_piece_volume(n, h, v):
    # Calculate the areas of the four pieces
    area1 = h * v
    area2 = h * (n - v)
    area3 = (n - h) * v
    area4 = (n - h) * (n - v)
    
    # Find the largest area
    max_area = max(area1, area2, area3, area4)
    
    # The thickness of the cake is 4 cm
    thickness = 4
    
    # Calculate the volume of the largest piece
    volume = max_area * thickness
    
    return volume

# Read input from stdin
import sys
input = sys.stdin.read
data = input().split()

# Parse the input values
n = int(data[0])
h = int(data[1])
v = int(data[2])

# Calculate and print the volume of the largest piece
print(largest_piece_volume(n, h, v))