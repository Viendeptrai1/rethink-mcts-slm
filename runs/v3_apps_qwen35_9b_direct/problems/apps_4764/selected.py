import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    h = int(input_data[1])
    v = int(input_data[2])
    
    # The cake is n x n with thickness 4.
    # Horizontal cut is at distance h from top, so it divides the height into h and (n - h).
    # Vertical cut is at distance v from left, so it divides the width into v and (n - v).
    
    # The four pieces have dimensions:
    # 1. Top-Left: h x v
    # 2. Top-Right: h x (n - v)
    # 3. Bottom-Left: (n - h) x v
    # 4. Bottom-Right: (n - h) x (n - v)
    
    # We need the maximum area among these four.
    areas = [
        h * v,
        h * (n - v),
        (n - h) * v,
        (n - h) * (n - v)
    ]
    
    max_area = max(areas)
    
    # Volume = Area * Thickness (4 cm)
    volume = max_area * 4
    
    print(volume)

if __name__ == "__main__":
    solve()