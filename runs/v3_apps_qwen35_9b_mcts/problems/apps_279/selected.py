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
    # For any second i, the speed s[i] must satisfy:
    # 1. s[i] <= v1 + i * d  (constraint from the start)
    # 2. s[i] <= v2 + (t - 1 - i) * d  (constraint from the end)
    # To maximize the total distance, we take the maximum possible speed at each second,
    # which is the minimum of these two upper bounds.

    total_distance = 0
    for i in range(t):
        max_from_start = v1 + i * d
        max_from_end = v2 + (t - 1 - i) * d
        current_speed = min(max_from_start, max_from_end)
        total_distance += current_speed

    print(total_distance)

if __name__ == "__main__":
    solve()