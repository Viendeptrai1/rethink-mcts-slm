def min_insertions_to_avoid_zero_sum_subarrays(n, arr):
    prefix_sums = {0: -1}
    current_sum = 0
    insertions = 0
    
    for i in range(n):
        current_sum += arr[i]
        
        if current_sum in prefix_sums:
            insertions += 1
            current_sum -= 1
        
        prefix_sums[current_sum] = i
    
    return insertions

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
arr = list(map(int, data[1:]))

print(min_insertions_to_avoid_zero_sum_subarrays(n, arr))