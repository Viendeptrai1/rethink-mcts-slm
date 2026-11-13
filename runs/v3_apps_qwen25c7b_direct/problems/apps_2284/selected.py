import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])

a = list(map(int, data[2:n+2]))
b = list(map(int, data[n+2:]))

# Sort indices based on the difference between preparation and printing costs
indices = sorted(range(n), key=lambda x: a[x] - b[x])

min_cost = float('inf')
for i in range(n-k+1):
    current_cost = sum(a[indices[j]] for j in range(i, i+k)) + sum(b[indices[j]] for j in range(i, i+k))
    min_cost = min(min_cost, current_cost)

print(min_cost)