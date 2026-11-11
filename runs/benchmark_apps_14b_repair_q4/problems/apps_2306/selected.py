import sys

def max_distance(N, times, velocities):
    def calculate_distance(t, v):
        # Calculate the maximum distance covered in time t with max speed v
        # The train can accelerate to v/2 in t/2 seconds, then maintain v for the rest
        if t <= v:
            # If time is less than or equal to max speed, it can reach max speed
            return (v * t) / 2
        else:
            # Otherwise, it accelerates to v/2, maintains v, and decelerates back to 0
            half_time = v / 2
            return (half_time * half_time) / 2 + (v * (t - half_time))

    total_distance = 0
    for i in range(N):
        total_distance += calculate_distance(times[i], velocities[i])

    return total_distance

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    times = list(map(int, data[1:N+1]))
    velocities = list(map(int, data[N+1:2*N+1]))
    
    result = max_distance(N, times, velocities)
    print(f"{result:.10f}")

if __name__ == "__main__":
    main()