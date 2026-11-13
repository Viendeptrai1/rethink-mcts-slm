def count_rectangles_with_sum(a, s):
    n = len(s)
    count = 0
    
    # Precompute the product matrix
    b = [[int(s[i]) * int(s[j]) for j in range(n)] for i in range(n)]
    
    # Precompute prefix sums for the product matrix
    prefix_sum = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            prefix_sum[i][j] = (prefix_sum[i - 1][j] + prefix_sum[i][j - 1] 
                                - prefix_sum[i - 1][j - 1] + b[i - 1][j - 1])
    
    # Count rectangles with sum equal to a
    for x in range(n):
        for y in range(x, n):
            for z in range(n):
                for t in range(z, n):
                    total = (prefix_sum[y + 1][t + 1] - prefix_sum[x][t + 1] 
                             - prefix_sum[y + 1][z] + prefix_sum[x][z])
                    if total == a:
                        count += 1
    
    return count

# Read input
a = int(input())
s = input().strip()

# Calculate and print the result
result = count_rectangles_with_sum(a, s)
print(result)