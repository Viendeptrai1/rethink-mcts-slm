def min_instability_after_removal(n, a):
    a.sort()
    # Calculate the instability for each possible removal
    min_instability = float('inf')
    for i in range(n):
        if i == 0:
            instability = a[n-1] - a[1]
        elif i == n-1:
            instability = a[n-2] - a[0]
        else:
            instability = max(a[i-1], a[n-1]) - min(a[0], a[i+1])
        min_instability = min(min_instability, instability)
    return min_instability

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
a = list(map(int, data[1:n+1]))

# Calculate and print the result
result = min_instability_after_removal(n, a)
print(result)