def longest_subarray_with_each_element_twice(arr):
    from collections import defaultdict
    
    n = len(arr)
    count = defaultdict(int)
    left = 0
    max_length = 0
    required_count = 2
    
    for right in range(n):
        count[arr[right]] += 1
        
        # If any element appears more than twice, shrink the window from the left
        while any(v > required_count for v in count.values()):
            count[arr[left]] -= 1
            if count[arr[left]] == 0:
                del count[arr[left]]
            left += 1
        
        # Check if all elements in the current window appear exactly twice
        if all(v == required_count for v in count.values()):
            max_length = max(max_length, right - left + 1)
    
    return max_length

# Read input
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
arr = list(map(int, data[1:]))

# Output the result
print(longest_subarray_with_each_element_twice(arr))