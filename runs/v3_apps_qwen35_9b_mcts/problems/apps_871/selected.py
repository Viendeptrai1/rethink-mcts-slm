import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    n = int(next(iterator))
    s = int(next(iterator))

    landings = []
    for _ in range(n):
        h = int(next(iterator))
        m = int(next(iterator))
        landings.append(h * 60 + m)

    # Check before the first landing
    # Takeoff needs 1 minute + s minutes before + s minutes after
    # So it occupies [t, t+1]
    # Constraint: t >= s (padding before) and t+1 + s <= first_landing (padding after)
    # => t <= first_landing - s - 1
    # We want earliest t >= 0.
    if s + 1 <= landings[0]:
        print(0, 0)
        return

    # Check between landings
    for i in range(n - 1):
        start_time = landings[i]
        end_time = landings[i + 1]
        
        # Landing i occupies [start_time, start_time + 1]
        # Landing i+1 occupies [end_time, end_time + 1]
        # Takeoff occupies [t, t+1]
        # Padding s before takeoff: t >= start_time + 1 + s
        # Padding s after takeoff: t + 1 + s <= end_time  => t <= end_time - s - 1
        
        min_t = start_time + 1 + s
        max_t = end_time - s - 1
        
        if min_t <= max_t:
            print(min_t // 60, min_t % 60)
            return

    # Check after the last landing
    last_landing = landings[-1]
    # Takeoff after last landing:
    # Padding s after last landing: t >= last_landing + 1 + s
    # No upper bound constraint from future landings (schedule ends)
    t = last_landing + 1 + s
    print(t // 60, t % 60)

if __name__ == "__main__":
    solve()