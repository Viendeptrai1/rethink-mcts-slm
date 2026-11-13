def max_cake_piece_volume(n, h, v):
    # Dimensions of the original cake
    thickness = 4
    
    # Dimensions of the pieces after cuts
    piece1 = (h * v * thickness)
    piece2 = ((n - h) * v * thickness)
    piece3 = (h * (n - v) * thickness)
    piece4 = ((n - h) * (n - v) * thickness)
    
    # Return the maximum volume among the four pieces
    return max(piece1, piece2, piece3, piece4)

# Example usage
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    h = int(data[1])
    v = int(data[2])
    print(max_cake_piece_volume(n, h, v))