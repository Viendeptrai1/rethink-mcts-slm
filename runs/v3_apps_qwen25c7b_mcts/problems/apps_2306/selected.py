import sys
input = sys.stdin.read
data = input().split()

N = int(data[0])
times = list(map(int, data[1:N+1]))
speeds = list(map(int, data[N+1:]))

def max_distance(t, v):
    half_time = t // 2
    return 0.5 * half_time * (half_time + 1) + v * (t - half_time)

total_distance = 0
for i in range(N):
    if speeds[i] == 0:
        continue
    if i == 0 or speeds[i-1] < speeds[i]:
        total_distance += max_distance(times[i], speeds[i])
    else:
        total_distance += max_distance(times[i], speeds[i]) - max_distance(times[i], speeds[i-1])

print(total_distance)