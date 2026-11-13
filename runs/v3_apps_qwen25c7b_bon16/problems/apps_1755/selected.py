def min_operations(n, k, a, b):
    if k == 0:
        return sum(1 for i in range(1, n) if a[i] <= a[i - 1])
    
    sorted_a = sorted(a)
    b_set = set(b)
    ops = 0
    
    for i in range(1, n):
        if a[i] <= a[i - 1]:
            if i + 1 in b_set:
                return -1
            target = sorted_a.index(a[i - 1]) + 1
            while a[i] <= a[i - 1]:
                a[i] = target
                target += 1
                ops += 1
    
    return ops

import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
a = list(map(int, data[2:n+2]))
b = list(map(int, data[n+2:n+2+k])) if k > 0 else []

print(min_operations(n, k, a, b))