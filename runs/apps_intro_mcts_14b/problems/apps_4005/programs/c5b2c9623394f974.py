import sys

def calculate_intersection_area(x1, y1, x2, y2, x3, y3, x4, y4):
    dx = min(x2, x4) - max(x1, x3)
    dy = min(y2, y4) - max(y1, y3)
    if dx > 0 and dy > 0:
        return dx * dy
    return 0

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    x1, y1, x2, y2 = map(int, data[:4])
    x3, y3, x4, y4 = map(int, data[4:8])
    x5, y5, x6, y6 = map(int, data[8:])
    
    white_sheet_area = (x2 - x1) * (y2 - y1)
    
    intersection1 = calculate_intersection_area(x1, y1, x2, y2, x3, y3, x4, y4)
    intersection2 = calculate_intersection_area(x1, y1, x2, y2, x5, y5, x6, y6)
    
    total_intersection_area = intersection1 + intersection2
    
    if total_intersection_area >= white_sheet_area:
        print("NO")
    else:
        print("YES")

if __name__ == "__main__":
    main()