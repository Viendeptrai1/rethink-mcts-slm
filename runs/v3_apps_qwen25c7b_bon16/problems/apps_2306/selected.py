def max_distance(N, t, v):
    total_distance = 0.0
    i = 0
    while i < N:
        # Acceleration phase
        acceleration_time = min(t[i], 2 * v[i])
        total_distance += 0.5 * v[i] * acceleration_time
        t[i] -= acceleration_time
        
        # Constant speed phase
        if t[i] > 0:
            total_distance += v[i] * t[i]
            t[i] = 0
        
        # Deceleration phase
        deceleration_time = min(t[i], 2 * v[i])
        total_distance += 0.5 * v[i] * deceleration_time
        t[i] -= deceleration_time
    
    return total_distance

# Read input
import sys
input = sys.stdin.read
data = input().split()

N = int(data[0])
t = list(map(int, data[1:N+1]))
v = list(map(int, data[N+1:]))

# Calculate and print the result
print(max_distance(N, t, v))