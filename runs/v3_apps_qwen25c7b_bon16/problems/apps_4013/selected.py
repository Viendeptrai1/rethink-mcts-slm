def min_instability_after_removal(a):
    a.sort()
    return min(a[-1] - a[1], a[-2] - a[0])

import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
a = list(map(int, data[1:]))

print(min_instability_after_removal(a))