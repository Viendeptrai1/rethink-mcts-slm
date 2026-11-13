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

    # Check if we can take off before the first landing
    # The first landing starts at landings[0].
    # We need 1 minute for takeoff + s minutes buffer after takeoff.
    # So takeoff must end by landings[0] - s - 1? 
    # Actually, the constraint is: distance between takeoff and landing >= s.
    # Takeoff occupies [t, t+1]. Landing occupies [l, l+1].
    # Distance between intervals [t, t+1] and [l, l+1] is min(|t - (l+1)|, |t+1 - l|).
    # Since landings are sorted and we consider t < l, the gap is l - (t+1).
    # We need l - (t+1) >= s  =>  t <= l - s - 1.
    # Also t >= 0.
    
    # Case 1: Before first landing
    if landings[0] >= s + 1:
        # Earliest time is 0
        print(0, 0)
        return

    # Case 2: Between landings
    for i in range(n - 1):
        l1 = landings[i]
        l2 = landings[i+1]
        # We need t such that:
        # 1. t >= l1 + 1 + s (buffer after landing 1)
        # 2. t + 1 + s <= l2 (buffer before landing 2) => t <= l2 - s - 1
        min_t = l1 + 1 + s
        max_t = l2 - s - 1
        
        if min_t <= max_t:
            print(min_t // 60, min_t % 60)
            return

    # Case 3: After last landing
    # We need t such that t >= landings[-1] + 1 + s
    t = landings[-1] + 1 + s
    print(t // 60, t % 60)

if __name__ == "__main__":
    solve()