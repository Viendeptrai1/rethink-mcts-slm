import sys
input = sys.stdin.read
data = input().split()

H = int(data[0])
W = int(data[1])
M = int(data[2])

targets = []
for i in range(M):
    h = int(data[3 + 2 * i]) - 1
    w = int(data[4 + 2 * i]) - 1
    targets.append((h, w))

rows = [0] * H
cols = [0] * W

for h, w in targets:
    rows[h] += 1
    cols[w] += 1

max_destroyed = max(rows) + max(cols)
print(max_destroyed)