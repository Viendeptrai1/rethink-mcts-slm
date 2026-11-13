import sys
input = sys.stdin.read
data = input().split()

H = int(data[0])
W = int(data[1])
M = int(data[2])

targets = [(int(data[3 + 2 * i]) - 1, int(data[4 + 2 * i]) - 1) for i in range(M)]

rows = [0] * H
cols = [0] * W

for h, w in targets:
    rows[h] += 1
    cols[w] += 1

max_destroyed = max(rows) + max(cols)

print(max_destroyed)