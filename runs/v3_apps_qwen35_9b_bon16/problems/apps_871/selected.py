import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        n = int(next(iterator))
        s = int(next(iterator))
    except StopIteration:
        return

    landings = []
    for _ in range(n):
        h = int(next(iterator))
        m = int(next(iterator))
        landings.append((h, m))

    def to_minutes(h, m):
        return h * 60 + m

    def minutes_to_time(total_minutes):
        h = total_minutes // 60
        m = total_minutes % 60
        return h, m

    current_time = 0

    for landing_h, landing_m in landings:
        landing_start = to_minutes(landing_h, landing_m)
        # The landing occupies [landing_start, landing_start + 1)
        # We need a gap of at least s minutes before and after the takeoff.
        # If we insert takeoff at time T (occupying [T, T+1)), then:
        # T >= landing_start + 1 + s  => T >= landing_start + s + 1
        
        earliest = landing_start + s + 1
        if current_time < earliest:
            current_time = earliest

    # After the last landing, we also need s minutes after the takeoff? 
    # Actually, the constraint is "between the takeoff and any landing".
    # So if the takeoff is the last event, there is no landing after it, so no constraint after.
    # But we must ensure the takeoff doesn't overlap with the last landing.
    # The loop above already handles the constraint "before the takeoff and after the landing" for all landings.
    # Specifically, for the last landing L_last, we ensured takeoff_start >= L_last_start + 1 + s.
    # This means the takeoff ends at takeoff_start + 1, and the gap between landing end (L_last_start+1) 
    # and takeoff start is (takeoff_start) - (L_last_start + 1) >= s. This satisfies the condition.
    
    # However, we must also consider if we can insert BEFORE the first landing.
    # The loop starts with current_time = 0. 
    # For the first landing at L1_start, we check if 0 < L1_start + s + 1.
    # If yes, current_time becomes L1_start + s + 1.
    # But wait, the problem says "earliest time". We should check if we can start at 0.
    # The condition for inserting at T=0 is: no landing in [0, s+1)? 
    # Actually, if we take off at 0, we occupy [0, 1). The first landing is at L1_start.
    # We need gap s between takeoff and landing.
    # Takeoff ends at 1. Landing starts at L1_start.
    # Gap = L1_start - 1. We need L1_start - 1 >= s => L1_start >= s + 1.
    # My logic in the loop: 
    #   earliest = L1_start + s + 1
    #   if current_time (0) < earliest: current_time = earliest
    # This sets current_time to L1_start + s + 1, which is WRONG if we can fit before.
    # The logic should be: we want the smallest T >= 0 such that for all landings i:
    #   T + 1 + s <= landing_start_i   OR   landing_end_i + s <= T
    # Since landings are sorted, we can just iterate and maintain the minimum valid T.
    
    # Let's restart the logic properly.
    # We want smallest T >= 0.
    # Constraints:
    # 1. For each landing i with start time L_i:
    #    If T < L_i, then we must have T + 1 + s <= L_i  => T <= L_i - s - 1
    #    If T > L_i, then we must have L_i + 1 + s <= T   => T >= L_i + s + 1
    #    (T cannot overlap L_i, so T cannot be in [L_i, L_i+1))
    
    # Since we want the earliest T, we can simulate minute by minute or use the gaps.
    # Given N <= 100, we can just check the gaps.
    
    # Valid intervals for T:
    # 1. Before the first landing: [0, L_0 - s - 1]. Earliest is 0 if L_0 - s - 1 >= 0.
    # 2. Between landing i and i+1: 
    #    Landing i ends at L_i + 1. Need gap s after landing i -> available starts at L_i + 1 + s.
    #    Landing i+1 starts at L_{i+1}. Need gap s before landing i+1 -> must end by L_{i+1} - s - 1.
    #    So valid range: [L_i + s + 1, L_{i+1} - s - 1].
    #    If start <= end, any T in this range works. Earliest is start.
    # 3. After the last landing:
    #    Last landing ends at L_{last} + 1. Need gap s after -> starts at L_{last} + 1 + s.
    #    No upper bound constraint from future landings. Earliest is L_{last} + s + 1.

    # Algorithm:
    # Check interval before first landing.
    # Check intervals between landings.
    # Check interval after last landing.
    # Pick the minimum valid T.

    candidates = []

    # Interval 1: Before first landing
    first_start = to_minutes(landings[0][0], landings[0][1])
    max_before = first_start - s - 1
    if max_before >= 0:
        candidates.append(0)

    # Intervals between landings
    for i in range(n - 1):
        start_land = to_minutes(landings[i][0], landings[i][1])
        end_land = start_land + 1
        
        next_start_land = to_minutes(landings[i+1][0], landings[i+1][1])
        
        # Earliest we can start after landing i is: end_land + s
        earliest_after = end_land + s
        # Latest we can start is such that it finishes before next landing minus s
        # T + 1 + s <= next_start_land => T <= next_start_land - s - 1
        latest_before = next_start_land - s - 1
        
        if earliest_after <= latest_before:
            candidates.append(earliest_after)

    # Interval after last landing
    last_start = to_minutes(landings[-1][0], landings[-1][1])
    earliest_after_last = last_start + s + 1
    candidates.append(earliest_after_last)

    min_t = min(candidates)
    
    h = min_t // 60
    m = min_t % 60
    print(f"{h} {m}")

if __name__ == "__main__":
    solve()