def max_cake_volume(n, h, v):
    # Calculate the dimensions of the four pieces of cake
    top_piece = h * v
    bottom_piece = (n - h) * v
    left_piece = h * (n - v)
    right_piece = (n - h) * (n - v)
    
    # Find the maximum volume among the four pieces
    max_volume = max(top_piece, bottom_piece, left_piece, right_piece)
    
    # The cake is 4 cm thick, so the volume in cubic centimeters is:
    max_volume_cm3 = max_volume * 4
    
    return max_volume_cm3

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().strip()
    n, h, v = map(int, data.split())
    print(max_cake_volume(n, h, v))