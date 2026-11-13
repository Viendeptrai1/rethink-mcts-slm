def max_cake_piece_volume(n, h, v):
    # Calculate the dimensions of the four pieces of cake
    piece1_area = h * v
    piece2_area = h * (n - v)
    piece3_area = (n - h) * v
    piece4_area = (n - h) * (n - v)
    
    # The volume of each piece is the area of the piece times the thickness of the cake
    cake_thickness = 4
    piece1_volume = piece1_area * cake_thickness
    piece2_volume = piece2_area * cake_thickness
    piece3_volume = piece3_area * cake_thickness
    piece4_volume = piece4_area * cake_thickness
    
    # Find the maximum volume among the four pieces
    max_volume = max(piece1_volume, piece2_volume, piece3_volume, piece4_volume)
    
    return max_volume

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().strip()
    n, h, v = map(int, data.split())
    print(max_cake_piece_volume(n, h, v))