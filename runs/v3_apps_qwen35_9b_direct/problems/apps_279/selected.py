import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    v1 = int(input_data[0])
    v2 = int(input_data[1])
    t = int(input_data[2])
    d = int(input_data[3])

    # We have t seconds. Let's index them from 0 to t-1.
    # Second 0 must have speed v1.
    # Second t-1 must have speed v2.
    # For any adjacent seconds i and i+1, |speed[i] - speed[i+1]| <= d.
    # We want to maximize sum(speed[i]) for i in 0..t-1.

    # For each second i, the maximum possible speed is constrained by:
    # 1. Starting from v1: speed[i] <= v1 + i * d
    # 2. Ending at v2: speed[i] <= v2 + (t - 1 - i) * d
    # The actual maximum speed at second i is the minimum of these two constraints.
    
    total_distance = 0
    for i in range(t):
        max_from_start = v1 + i * d
        max_from_end = v2 + (t - 1 - i) * d
        current_max = min(max_from_start, max_from_end)
        total_distance += current_max

    print(total_distance)

if __name__ == "__main__":
    solve()