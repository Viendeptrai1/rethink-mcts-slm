def min_rolls_to_score(x):
    return x // 2

import sys
input = sys.stdin.read
data = input().split()

t = int(data[0])
results = []

for i in range(1, t + 1):
    x = int(data[i])
    results.append(min_rolls_to_score(x))

print(*results, sep='\n')