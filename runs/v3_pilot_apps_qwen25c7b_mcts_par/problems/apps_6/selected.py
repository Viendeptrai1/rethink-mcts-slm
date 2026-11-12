import sys
input = sys.stdin.read
data = input().split()

def solve(n, x, blows):
    blows.sort(key=lambda b: (b[0] - b[1], b[0]))
    total_blows = 0
    while x > 0:
        found = False
        for d, h in blows:
            if d >= x:
                total_blows += 1
                x = 0
                found = True
                break
            else:
                x -= min(d, x)
                x += h
        if not found:
            return -1
    return total_blows

t = int(data[0])
index = 1
results = []
for _ in range(t):
    n = int(data[index])
    x = int(data[index + 1])
    index += 2
    blows = []
    for _ in range(n):
        d = int(data[index])
        h = int(data[index + 1])
        index += 2
        blows.append((d, h))
    results.append(solve(n, x, blows))

for result in results:
    print(result)