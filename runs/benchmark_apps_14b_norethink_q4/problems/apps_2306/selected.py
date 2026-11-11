import sys

def max_distance(N, times, speeds):
    def calculate_segment_distance(t, v):
        # Calculate the maximum distance for a single segment
        if t <= v:
            # If time is less than or equal to speed, we can accelerate to full speed and then decelerate
            return (v * v) / 2
        else:
            # Otherwise, we can accelerate to full speed, maintain, and then decelerate
            accelerate_time = v
            maintain_time = t - 2 * v
            if maintain_time < 0:
                # If there's not enough time to maintain full speed, adjust the times
                accelerate_time = t / 2
                maintain_time = 0
            return (accelerate_time * accelerate_time) / 2 + maintain_time * v + (accelerate_time * accelerate_time) / 2

    total_distance = 0
    for i in range(N):
        total_distance += calculate_segment_distance(times[i], speeds[i])

    return total_distance

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    times = list(map(int, data[1:N+1]))
    speeds = list(map(int, data[N+1:2*N+1]))
    
    result = max_distance(N, times, speeds)
    print(f"{result:.15f}")

if __name__ == "__main__":
    main()