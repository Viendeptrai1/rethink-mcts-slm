def min_cost_to_make_white(n, m, rectangles):
    # Initialize a 2D array to keep track of the number of black cells in each row and column
    row_black = [0] * (n + 1)
    col_black = [0] * (n + 1)

    # Process each rectangle to update the row and column black counts
    for x1, y1, x2, y2 in rectangles:
        row_black[x1 - 1] += 1
        row_black[x2] -= 1
        col_black[y1 - 1] += 1
        col_black[y2] -= 1

    # Calculate the prefix sums to get the actual number of black cells in each row and column
    for i in range(1, n):
        row_black[i] += row_black[i - 1]
    for j in range(1, n):
        col_black[j] += col_black[j - 1]

    # Calculate the total number of black cells
    total_black_cells = sum(row_black[i] > 0 for i in range(n)) * sum(col_black[j] > 0 for j in range(n))

    # The minimum cost is the number of black cells, as each cell can be turned white at a cost of 1
    return total_black_cells

# Read input
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

# Calculate and print the result
result = min_cost_to_make_white(n, m, rectangles)
print(result)