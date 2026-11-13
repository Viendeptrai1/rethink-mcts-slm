def find_divisible_number(n, arr):
    min_val = min(arr)
    for num in arr:
        if num % min_val != 0:
            return -1
    return min_val

# Input reading
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
arr = list(map(int, data[1:]))

# Output the result
print(find_divisible_number(n, arr))