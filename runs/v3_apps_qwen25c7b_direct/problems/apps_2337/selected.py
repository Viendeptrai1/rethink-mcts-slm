def min_problems_to_add(n, m, a, b):
    missing = [0] * n
    j = 0
    for i in range(n):
        while j < m and b[j] < a[i]:
            j += 1
        if j == m or b[j] > a[i]:
            missing[i] = 1
    return sum(missing)

# Example usage:
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
a = list(map(int, data[2:n+2]))
b = list(map(int, data[n+2:]))

print(min_problems_to_add(n, m, a, b))