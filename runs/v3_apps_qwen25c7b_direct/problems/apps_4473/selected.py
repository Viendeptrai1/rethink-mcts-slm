def frog_position(a, b, k):
    if k % 2 == 0:
        return 0
    else:
        if k % 4 == 1:
            return a
        elif k % 4 == 3:
            return -b

import sys
input = sys.stdin.read
data = input().split()

t = int(data[0])
results = []

index = 1
for _ in range(t):
    a = int(data[index])
    b = int(data[index + 1])
    k = int(data[index + 2])
    index += 3
    results.append(frog_position(a, b, k))

print('\n'.join(map(str, results)))