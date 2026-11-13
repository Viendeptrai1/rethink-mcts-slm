def max_piece_volume(n, h, v):
    # Calculate the dimensions of the four resulting pieces
    piece1 = h * v * 4
    piece2 = (n - h) * v * 4
    piece3 = h * (n - v) * 4
    piece4 = (n - h) * (n - v) * 4
    
    # Return the maximum volume among the four pieces
    return max(piece1, piece2, piece3, piece4)

# Read input values
n, h, v = map(int, input().split())

# Print the volume of the largest piece
print(max_piece_volume(n, h, v))