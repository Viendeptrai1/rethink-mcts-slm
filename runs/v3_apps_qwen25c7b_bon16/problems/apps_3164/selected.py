def longest_subarray(N, arr):
    max_length = 0
    left = 0
    count = {}

    for right in range(N):
        if arr[right] in count:
            count[arr[right]] += 1
        else:
            count[arr[right]] = 1

        while all(v == 2 for v in count.values()):
            max_length = max(max_length, right - left + 1)
            count[arr[left]] -= 1
            if count[arr[left]] == 0:
                del count[arr[left]]
            left += 1

    return max_length

# Input reading
import sys
input = sys.stdin.read
data = input().split()
N = int(data[0])
arr = list(map(int, data[1:]))

# Output result
print(longest_subarray(N, arr))