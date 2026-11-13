import sys
input = sys.stdin.read
data = input().split()

N = int(data[0])
t = list(map(int, data[1:N+1]))
v = list(map(int, data[N+1:]))

max_distance = 0

for i in range(N):
    if i == 0:
        # Accelerate to v[i] over t[i] seconds
        max_distance += (v[i] * v[i]) / 2
    elif i == N-1:
        # Decelerate to 0 over t[i] seconds
        max_distance += (v[i-1] * v[i-1]) / 2
    else:
        # Maintain constant speed v[i] over t[i] seconds
        max_distance += v[i] * t[i]

print(max_distance)