def is_sorted(arr):
    return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))

def thanos_sort_max_length(arr):
    n = len(arr)
    if n == 1 or is_sorted(arr):
        return n
    
    mid = n // 2
    left_half = arr[:mid]
    right_half = arr[mid:]
    
    # Option 1: Remove the first half
    max_length_left = thanos_sort_max_length(right_half)
    
    # Option 2: Remove the second half
    max_length_right = thanos_sort_max_length(left_half)
    
    return max(max_length_left, max_length_right)

import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
arr = list(map(int, data[1:]))

print(thanos_sort_max_length(arr))