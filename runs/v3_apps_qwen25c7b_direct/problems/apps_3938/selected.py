def min_cost_to_paint_white(n, m, rectangles):
    # Sort rectangles by their height and then by their width
    rectangles.sort(key=lambda r: (r[3] - r[1], r[2] - r[0]))
    
    # Initialize variables
    cost = 0
    current_rectangles = []
    
    for rect in rectangles:
        x1, y1, x2, y2 = rect
        
        # Remove overlapping rectangles that are already covered
        current_rectangles = [r for r in current_rectangles if not (x1 >= r[2] or x2 <= r[0] or y1 >= r[3] or y2 <= r[1])]
        
        # Add the new rectangle to the list
        current_rectangles.append(rect)
        
        # Calculate the cost for this step
        h = max(r[3] - r[1] for r in current_rectangles)
        w = max(r[2] - r[0] for r in current_rectangles)
        cost += min(h, w)
    
    return cost

# Example usage:
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

print(min_cost_to_paint_white(n, m, rectangles))