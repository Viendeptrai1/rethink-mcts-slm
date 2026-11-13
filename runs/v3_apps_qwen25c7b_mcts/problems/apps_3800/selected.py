import sys

def count_rectangles(a, s):
    n = len(s)
    count = 0
    
    # Precompute prefix sums of products
    prefix_sum = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            prefix_sum[i][j] = prefix_sum[i - 1][j] + prefix_sum[i][j - 1] - prefix_sum[i - 1][j - 1] + int(s[j - 1]) * int(s[i - 1])
    
    # Check all possible rectangles
    for x in range(n):
        for y in range(x + 1, n + 1):
            for z in range(n):
                for t in range(z + 1, n + 1):
                    if prefix_sum[y][t] - prefix_sum[x][t] - prefix_sum[y][z] + prefix_sum[x][z] == a:
                        count += 1
    
    return count

# Read input
input = sys.stdin.read
data = input().split()
a = int(data[0])
s = data[1]

# Output result
print(count_rectangles(a, s))