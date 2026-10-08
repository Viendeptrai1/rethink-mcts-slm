import sys
from itertools import combinations

def max_calm_group_sum(n, a, b):
    max_sum = 0
    
    # Check all pairs of students
    for i in range(n):
        for j in range(i + 1, n):
            if (a[i] & a[j] != a[i]) and (a[i] & a[j] != a[j]):
                max_sum = max(max_sum, b[i] + b[j])
    
    return max_sum

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
a = list(map(int, data[1:n+1]))
b = list(map(int, data[n+1:2*n+1]))

# Output the result
print(max_calm_group_sum(n, a, b))