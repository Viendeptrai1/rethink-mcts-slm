import sys
from typing import List, Tuple

def min_cost_to_paint_white(n: int, m: int, rectangles: List[Tuple[int, int, int, int]]) -> int:
    # Sort rectangles by area in descending order
    rectangles.sort(key=lambda rect: (rect[2] - rect[0] + 1) * (rect[3] - rect[1] + 1), reverse=True)
    
    total_cost = 0
    
    while rectangles:
        # Take the largest rectangle
        x1, y1, x2, y2 = rectangles.pop(0)
        height = x2 - x1 + 1
        width = y2 - y1 + 1
        cost = min(height, width)
        total_cost += cost
        
        # Remove the effect of this rectangle from other rectangles
        new_rectangles = []
        for rx1, ry1, rx2, ry2 in rectangles:
            # Calculate the intersection of the current rectangle with the new one
            ix1 = max(x1, rx1)
            iy1 = max(y1, ry1)
            ix2 = min(x2, rx2)
            iy2 = min(y2, ry2)
            
            if ix1 <= ix2 and iy1 <= iy2:
                # If there is an intersection, split the rectangle into smaller parts
                if ix1 > rx1:
                    new_rectangles.append((rx1, ry1, ix1 - 1, ry2))
                if ix2 < rx2:
                    new_rectangles.append((ix2 + 1, ry1, rx2, ry2))
                if iy1 > ry1:
                    new_rectangles.append((max(ix1, rx1), ry1, min(ix2, rx2), iy1 - 1))
                if iy2 < ry2:
                    new_rectangles.append((max(ix1, rx1), iy2 + 1, min(ix2, rx2), ry2))
        
        rectangles = new_rectangles
    
    return total_cost

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    rectangles = []
    
    index = 2
    for _ in range(m):
        x1 = int(data[index])
        y1 = int(data[index + 1])
        x2 = int(data[index + 2])
        y2 = int(data[index + 3])
        rectangles.append((x1, y1, x2, y2))
        index += 4
    
    result = min_cost_to_paint_white(n, m, rectangles)
    print(result)

if __name__ == "__main__":
    main()