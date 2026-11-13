def max_erased_elements(n, a):
    max_erased = 0
    current_max_erased = 0
    
    for i in range(1, n):
        if a[i] == a[i - 1] + 1:
            current_max_erased += 1
            max_erased = max(max_erased, current_max_erased)
        else:
            current_max_erased = 0
            
    return max_erased

# Input reading
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
a = list(map(int, data[1:]))

# Output the result
print(max_erased_elements(n, a))