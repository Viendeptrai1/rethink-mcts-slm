import sys

def min_cost_to_paint_white(n, m, rectangles):
    # Initialize the cost to 0
    total_cost = 0
    
    # Iterate over each rectangle
    for x1, y1, x2, y2 in rectangles:
        # Calculate the height and width of the rectangle
        h = x2 - x1 + 1
        w = y2 - y1 + 1
        # Add the minimum of height and width to the total cost
        total_cost += min(h, w)
    
    return total_cost

# Read input from stdin
input = sys.stdin.read
data = input().split()

# Parse the input values
n = int(data[0])
m = int(data[1])
rectangles = []

# Read the rectangles
index = 2
for _ in range(m):
    x1 = int(data[index])
    y1 = int(data[index + 1])
    x2 = int(data[index + 2])
    y2 = int(data[index + 3])
    rectangles.append((x1, y1, x2, y2))
    index += 4

# Calculate the minimum cost to paint the whole square in white
result = min_cost_to_paint_white(n, m, rectangles)

# Print the result
print(result)