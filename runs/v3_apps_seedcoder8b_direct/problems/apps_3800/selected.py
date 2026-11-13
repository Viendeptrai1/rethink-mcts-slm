def count_rectangles_with_sum(a, s):
    n = len(s)
    s = list(map(int, s))
    
    # Precompute the prefix sums for the matrix b
    prefix_sum = [[0] * (n + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            prefix_sum[i][j] = s[i - 1] * s[j - 1] + prefix_sum[i - 1][j] + prefix_sum[i][j - 1] - prefix_sum[i - 1][j - 1]
    
    count = 0
    
    # Iterate over all possible top-left corners (x, z)
    for x in range(1, n + 1):
        for z in range(1, n + 1):
            # Iterate over all possible bottom-right corners (y, t)
            for y in range(x, n + 1):
                for t in range(z, n + 1):
                    # Calculate the sum of the rectangle using the prefix sums
                    total = (prefix_sum[y][t]
                             - prefix_sum[x - 1][t]
                             - prefix_sum[y][z - 1]
                             + prefix_sum[x - 1][z - 1])
                    if total == a:
                        count += 1
    
    return count

# Read input
import sys
input = sys.stdin.read
data = input().split()
a = int(data[0])
s = data[1]

# Get the result and print it
result = count_rectangles_with_sum(a, s)
print(result)