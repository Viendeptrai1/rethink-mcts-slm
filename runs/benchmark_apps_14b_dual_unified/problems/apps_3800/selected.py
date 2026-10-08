import sys

def count_rectangles(a, s):
    n = len(s)
    count = 0
    
    # Precompute the product matrix b
    b = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            b[i][j] = int(s[i]) * int(s[j])
    
    # Check all possible rectangles
    for x in range(n):
        for y in range(x, n):
            for z in range(n):
                for t in range(z, n):
                    total_sum = 0
                    for i in range(x, y + 1):
                        for j in range(z, t + 1):
                            total_sum += b[i][j]
                    if total_sum == a:
                        count += 1
    
    return count

# Read input
a = int(sys.stdin.readline().strip())
s = sys.stdin.readline().strip()

# Output the result
print(count_rectangles(a, s))