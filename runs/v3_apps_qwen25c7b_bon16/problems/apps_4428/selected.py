def max_sum_split(d):
    total_sum = sum(d)
    if total_sum % 2 != 0:
        return 0
    
    target = total_sum // 2
    left_sum = 0
    best_sum = 0
    
    for num in d:
        left_sum += num
        if left_sum == target:
            best_sum = target
        elif left_sum > target:
            break
    
    return best_sum

# Input reading
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
d = list(map(int, data[1:]))

# Output result
print(max_sum_split(d))