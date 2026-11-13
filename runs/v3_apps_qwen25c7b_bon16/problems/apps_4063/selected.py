from typing import List
import sys
input = sys.stdin.read
data = input().split()
N = int(data[0])
d = list(map(int, data[1:]))

# Sort the difficulties
d.sort()

# Use binary search to find the number of valid K values
left, right = 0, N
while left < right:
    mid = (left + right) // 2
    if sum(1 for x in d if x >= d[mid]) == N // 2:
        left = mid + 1
    else:
        right = mid

print(left)