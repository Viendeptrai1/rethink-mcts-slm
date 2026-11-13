def can_reorder(a):
    n = len(a) // 2
    total_sum = sum(a)
    if total_sum % 2 != 0:
        return -1
    
    target_sum = total_sum // 2
    current_sum = 0
    result = []
    
    for i in range(2 * n):
        if current_sum + a[i] <= target_sum:
            current_sum += a[i]
            result.append(a[i])
        else:
            result.insert(0, a[i])
    
    if current_sum == target_sum:
        return result
    else:
        return -1

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
a = list(map(int, data[1:]))

# Output result
result = can_reorder(a)
if result == -1:
    print(-1)
else:
    print(' '.join(map(str, result)))