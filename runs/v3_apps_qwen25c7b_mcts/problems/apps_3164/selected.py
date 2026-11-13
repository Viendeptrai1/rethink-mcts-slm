def longest_subarray_with_two_occurrences(n, arr):
    count = {}
    left = 0
    max_length = 0
    
    for right in range(n):
        if arr[right] in count:
            count[arr[right]] += 1
        else:
            count[arr[right]] = 1
        
        while count[arr[right]] > 2:
            count[arr[left]] -= 1
            if count[arr[left]] == 0:
                del count[arr[left]]
            left += 1
        
        if len(count) == 2:
            max_length = max(max_length, right - left + 1)
    
    return max_length

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
arr = list(map(int, data[1:]))

print(longest_subarray_with_two_occurrences(n, arr))