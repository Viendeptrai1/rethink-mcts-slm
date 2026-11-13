def min_cost_to_paint_white(n, m, rectangles):
    # Initialize a 2D difference array to track changes in black cell counts
    diff = [[0] * (n + 2) for _ in range(n + 2)]

    # Apply the difference array technique to mark black rectangles
    for x1, y1, x2, y2 in rectangles:
        diff[x1][y1] += 1
        diff[x1][y2 + 1] -= 1
        diff[x2 + 1][y1] -= 1
        diff[x2 + 1][y2 + 1] += 1

    # Calculate the prefix sum to get the actual black cell counts
    black_count = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            black_count[i][j] = (diff[i][j] + black_count[i - 1][j] +
                                 black_count[i][j - 1] - black_count[i - 1][j - 1])

    # Calculate the minimum cost to paint the whole grid white
    min_cost = 0
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if black_count[i][j] > 0:
                # Find the maximum rectangle that covers this black cell
                max_i, max_j = i, j
                while max_i <= n and black_count[max_i][j] > 0:
                    max_i += 1
                while max_j <= n and black_count[i][max_j] > 0:
                    max_j += 1
                # Calculate the cost for this rectangle
                min_cost += min(max_i - i, max_j - j)
                # Mark this rectangle as covered
                for x in range(i, max_i):
                    for y in range(j, max_j):
                        black_count[x][y] = 0

    return min_cost

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

# Get the result
result = min_cost_to_paint_white(n, m, rectangles)

# Print the result
print(result)