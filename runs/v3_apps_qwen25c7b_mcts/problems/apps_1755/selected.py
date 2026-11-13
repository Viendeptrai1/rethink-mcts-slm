def min_operations(n, k, a, b):
    if k == 0:
        return max(0, sum(a[i] >= a[i + 1] for i in range(n - 1)))
    
    b_set = set(b)
    operations = 0
    
    for i in range(n - 1):
        if a[i] >= a[i + 1]:
            if i + 1 in b_set:
                return -1
            operations += a[i] - a[i + 1] + 1
            a[i + 1] = a[i] + 1
    
    return operations

# Input reading
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
a = list(map(int, data[2:n+2]))
if k > 0:
    b = list(map(int, data[n+2:n+k+2]))
else:
    b = []

# Output result
print(min_operations(n, k, a, b))