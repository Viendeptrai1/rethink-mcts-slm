import sys

def max_symmetric_matrix(n, k):
    if k > n * n // 2:
        return -1
    
    result = [[0] * n for _ in range(n)]
    
    # Place the maximum possible number of ones on the upper triangle
    count = 0
    for i in range(n):
        for j in range(i + 1):
            if count < k:
                result[i][j] = 1
                result[j][i] = 1
                count += 1
            else:
                break
    
    return result

# Read input
n, k = map(int, sys.stdin.readline().split())

# Get the result
result = max_symmetric_matrix(n, k)

# Print the result
if result == -1:
    print(-1)
else:
    for row in result:
        print(' '.join(map(str, row)))