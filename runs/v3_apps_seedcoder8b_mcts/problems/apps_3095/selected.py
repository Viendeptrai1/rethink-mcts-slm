def largest_extremely_cool_submatrix(R, S, matrix):
    # Initialize a 3D DP array to store the maximum size of cool submatrices
    dp = [[[0] * (S + 1) for _ in range(S + 1)] for _ in range(R + 1)]

    max_elements = 0

    # Iterate over all possible submatrices
    for r in range(2, R + 1):
        for s in range(2, S + 1):
            for i in range(1, R - r + 2):
                for j in range(1, S - s + 2):
                    # Check if the current submatrix is cool
                    if matrix[i - 1][j - 1] + matrix[i + r - 2][j + s - 2] <= matrix[i - 1][j + s - 2] + matrix[i + r - 2][j - 1]:
                        # Update the DP table
                        dp[i][j][s] = max(dp[i][j][s], dp[i + 1][j + 1][s - 2] + r * s)
                        max_elements = max(max_elements, dp[i][j][s])

    return max_elements

# Read input
import sys
input = sys.stdin.read
data = input().split()

R = int(data[0])
S = int(data[1])
matrix = []

index = 2
for _ in range(R):
    row = list(map(int, data[index:index + S]))
    matrix.append(row)
    index += S

# Get the result
result = largest_extremely_cool_submatrix(R, S, matrix)

# Print the result
print(result)