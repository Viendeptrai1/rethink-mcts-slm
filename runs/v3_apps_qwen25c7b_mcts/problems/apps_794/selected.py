def can_partition(n, a):
    a.sort()
    left_sum = 0
    right_sum = sum(a)
    
    for i in range(n):
        left_sum += a[i]
        right_sum -= a[i]
        
        if left_sum != right_sum:
            return ' '.join(map(str, a))
    
    return '-1'

# Input reading
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
a = list(map(int, data[1:]))

# Output result
print(can_partition(n, a))