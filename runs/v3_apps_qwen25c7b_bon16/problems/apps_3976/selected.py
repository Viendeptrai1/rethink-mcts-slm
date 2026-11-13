from collections import Counter

def valid_positions(n, m, p, a, b):
    count_b = Counter(b)
    results = []

    for q in range(1, n - m * p + 2):
        if Counter(a[q-1:q-1+m*p:p]) == count_b:
            results.append(q)

    return len(results), results

# Input reading
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
p = int(data[2])

a = list(map(int, data[3:n+3]))
b = list(map(int, data[n+3:]))

# Output
result_count, result_values = valid_positions(n, m, p, a, b)
print(result_count)
print(' '.join(map(str, result_values)))