import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    h = int(input_data[1])
    v = int(input_data[2])
    
    # The cuts divide the square into four rectangles with dimensions:
    # Top-Left: h x v
    # Top-Right: h x (n - v)
    # Bottom-Left: (n - h) x v
    # Bottom-Right: (n - h) x (n - v)
    
    # Calculate the four areas
    area1 = h * v
    area2 = h * (n - v)
    area3 = (n - h) * v
    area4 = (n - h) * (n - v)
    
    # Find the maximum area
    max_area = max(area1, area2, area3, area4)
    
    # The cake is 4 cm thick, so volume = max_area * 4
    volume = max_area * 4
    
    print(volume)

if __name__ == "__main__":
    solve()