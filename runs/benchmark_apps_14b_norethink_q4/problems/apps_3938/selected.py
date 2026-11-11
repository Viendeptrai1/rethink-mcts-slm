import sys
from typing import List, Tuple

def min_painting_cost(n: int, m: int, rectangles: List[Tuple[int, int, int, int]]) -> int:
    # Sort rectangles by area (height * width)
    rectangles.sort(key=lambda rect: (rect[2] - rect[0] + 1) * (rect[3] - rect[1] + 1))
    
    # Initialize the cost
    total_cost = 0
    
    # Iterate over each rectangle
    for x1, y1, x2, y2 in rectangles:
        # Calculate the height and width of the rectangle
        height = x2 - x1 + 1
        width = y2 - y1 + 1
        
        # Add the minimum of height and width to the total cost
        total_cost += min(height, width)
    
    return total_cost

# Read input
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

# Calculate and print the result
result = min_painting_cost(n, m, rectangles)
print(result)