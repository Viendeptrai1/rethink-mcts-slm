def max_erased_elements(n, a):
    if n <= 1:
        return 0
    
    max_gap = 1
    current_gap = 1
    
    for i in range(1, n):
        if a[i] == a[i-1] + 1:
            current_gap += 1
        else:
            max_gap = max(max_gap, current_gap)
            current_gap = 1
    
    max_gap = max(max_gap, current_gap)
    
    if max_gap > 2:
        return max_gap - 2
    elif max_gap == 2:
        return 1
    else:
        return 0

# Example usage:
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
a = list(map(int, data[1:]))

print(max_erased_elements(n, a))