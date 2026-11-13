def min_i(n, k, A):
    i = 0
    while True:
        if max(A) >= k:
            return i
        A = [sum(A[:j+1]) for j in range(n)]
        i += 1

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])
A = list(map(int, data[2:]))

result = min_i(n, k, A)
print(result)