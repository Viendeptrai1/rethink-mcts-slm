def max_distance(N, times, speeds):
    max_distance = 0.0

    for i in range(N):
        t = times[i]
        v = speeds[i]

        # Accelerating phase
        max_distance += (v ** 2) / (2 * 1)

        # Constant speed phase
        max_distance += v * (t - 2)

        # Decelerating phase
        max_distance += (v ** 2) / (2 * 1)

    return max_distance

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().strip().split()
    
    N = int(data[0])
    times = list(map(int, data[1:N+1]))
    speeds = list(map(int, data[N+1:2*N+1]))
    
    result = max_distance(N, times, speeds)
    print(f"{result:.15f}")