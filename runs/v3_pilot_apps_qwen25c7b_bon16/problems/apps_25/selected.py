def create_symmetric_matrix(n, k):
    if k > n * (n + 1) // 2:
        return -1
    
    result = [[0] * n for _ in range(n)]
    
    i, j = 0, 0
    while k > 0:
        if i == j:
            result[i][j] = 1
            k -= 1
        elif result[i][j] == 0:
            result[i][j] = 1
            result[j][i] = 1
            k -= 2
        i += 1
        if i == n:
            i = 0
            j += 1
    
    return result

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])

# Create symmetric matrix
result = create_symmetric_matrix(n, k)

# Print result
if result == -1:
    print(-1)
else:
    for row in result:
        print(' '.join(map(str, row)))