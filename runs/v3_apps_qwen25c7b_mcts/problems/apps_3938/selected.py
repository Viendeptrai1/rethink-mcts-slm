def min_cost_to_paint(n, m, rectangles):
    if m == 0:
        return 0
    
    # Find the bounding box of all black rectangles
    min_x = min(rect[0] for rect in rectangles)
    max_x = max(rect[2] for rect in rectangles)
    min_y = min(rect[1] for rect in rectangles)
    max_y = max(rect[3] for rect in rectangles)
    
    # The cost to paint the entire bounding box
    h = max_y - min_y + 1
    w = max_x - min_x + 1
    return min(h, w)

# Example usage:
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])

rectangles = []
for i in range(m):
    x1 = int(data[2 + i * 4])
    y1 = int(data[3 + i * 4])
    x2 = int(data[4 + i * 4])
    y2 = int(data[5 + i * 4])
    rectangles.append((x1, y1, x2, y2))

print(min_cost_to_paint(n, m, rectangles))