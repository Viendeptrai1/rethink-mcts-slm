def find_missing_vertices(x1, y1, x2, y2):
    # Calculate the vector from (x1, y1) to (x2, y2)
    a = x2 - x1
    b = y2 - y1
    
    # Rotate the vector (a, b) by 90 degrees counter-clockwise to get (-b, a)
    rotated_a = -b
    rotated_b = a
    
    # Calculate the third vertex (x3, y3)
    x3 = x2 + rotated_a
    y3 = y2 + rotated_b
    
    # Calculate the fourth vertex (x4, y4)
    x4 = x1 + rotated_a
    y4 = y1 + rotated_b
    
    return x3, y3, x4, y4

# Read input
x1, y1, x2, y2 = map(int, input().split())

# Find the missing vertices
x3, y3, x4, y4 = find_missing_vertices(x1, y1, x2, y2)

# Print the result
print(x3, y3, x4, y4)