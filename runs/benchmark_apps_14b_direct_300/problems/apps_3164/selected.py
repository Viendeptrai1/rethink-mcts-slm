def longest_subarray_with_each_element_twice(arr):
    from collections import defaultdict
    
    n = len(arr)
    count = defaultdict(int)
    left = 0
    max_length = 0
    
    for right in range(n):
        count[arr[right]] += 1
        
        while count[arr[right]] > 2:
            count[arr[left]] -= 1
            left += 1
        
        if all(v == 2 for v in count.values()):
            max_length = max(max_length, right - left + 1)
    
    return max_length

# Read input
import sys
input = sys.stdin.read
data = input().split()

N = int(data[0])
arr = list(map(int, data[1:]))

# Output the result
print(longest_subarray_with_each_element_twice(arr))