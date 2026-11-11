import sys
from typing import List, Tuple

def min_cost_to_paint_white(n: int, m: int, rectangles: List[Tuple[int, int, int, int]]) -> int:
    # Initialize the cost to 0
    total_cost = 0
    
    # Iterate over each rectangle
    for x1, y1, x2, y2 in rectangles:
        # Calculate the height and width of the rectangle
        height = x2 - x1 + 1
        width = y2 - y1 + 1
        
        # Add the minimum of height and width to the total cost
        total_cost += min(height, width)
    
    return total_cost

# Read input from stdin
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