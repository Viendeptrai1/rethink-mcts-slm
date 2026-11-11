import sys

def max_distance(N, t, v):
    def calculate_distance(t_i, v_i):
        # Calculate the maximum distance for a single segment
        if v_i * v_i <= 2 * t_i:
            # If we can reach the full speed within the time
            return (v_i * v_i) / 2
        else:
            # Otherwise, we accelerate to the maximum possible speed
            t_accel = v_i
            d_accel = (t_accel * t_accel) / 2
            t_const = t_i - 2 * t_accel
            d_const = v_i * t_const
            return d_accel + d_const

    total_distance = 0
    for i in range(N):
        total_distance += calculate_distance(t[i], v[i])

    return total_distance

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    t = list(map(int, data[1:N+1]))
    v = list(map(int, data[N+1:2*N+1]))
    
    result = max_distance(N, t, v)
    print(f"{result:.15f}")

if __name__ == "__main__":
    main()