def largest_k_multiple_free_subset(n, k, arr):
    arr.sort()
    last_seen = {}
    result = []
    
    for num in arr:
        if num % k != 0 or num // k not in last_seen:
            result.append(num)
            last_seen[num] = len(result) - 1
    
    return len(result)

# Example usage:
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
arr = list(map(int, data[2:]))

print(largest_k_multiple_free_subset(n, k, arr))