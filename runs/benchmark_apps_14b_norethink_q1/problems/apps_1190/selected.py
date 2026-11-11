import sys

def calculate_marked_cells(w1, h1, w2, h2):
    # Calculate the number of marked cells around the first rectangle
    marked_around_first = 2 * (w1 + h1) + 4
    
    # Calculate the number of marked cells around the second rectangle
    marked_around_second = 2 * (w2 + h2) + 4
    
    # Calculate the overlap area
    # The overlap includes the vertical edges and possibly the horizontal edges
    overlap = 2 * (w2 + 1) + 2 * (h2 + 1) - 4
    
    # Total marked cells is the sum of marked cells around both rectangles minus the overlap
    total_marked = marked_around_first + marked_around_second - overlap
    
    return total_marked

# Read input
input = sys.stdin.read
data = input().split()
w1 = int(data[0])
h1 = int(data[1])
w2 = int(data[2])
h2 = int(data[3])

# Calculate and print the result
result = calculate_marked_cells(w1, h1, w2, h2)
print(result)