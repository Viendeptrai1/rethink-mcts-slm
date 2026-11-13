def min_moves_to_sort(n, p):
    inversions = 0
    for i in range(n):
        for j in range(i + 1, n):
            if p[i] > p[j]:
                inversions += 1
    return inversions

# Input reading
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
p = list(map(int, data[1:]))

# Output the result
print(min_moves_to_sort(n, p))