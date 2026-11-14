import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        Tg = int(next(iterator))
        Ty = int(next(iterator))
        Tr = int(next(iterator))
        n = int(next(iterator))
        
        observations = []
        for _ in range(n):
            t = int(next(iterator))
            c = next(iterator)
            observations.append((t, c))
            
        tq = int(next(iterator))
        cq = next(iterator)
        
    except StopIteration:
        return

    total_cycle = Tg + Ty + Tr

    # Define the color intervals within [0, total_cycle)
    # Green: [0, Tg)
    # Yellow: [Tg, Tg + Ty)
    # Red: [Tg + Ty, total_cycle)
    
    def get_color_interval(color):
        if color == 'green':
            return (0, Tg)
        elif color == 'yellow':
            return (Tg, Tg + Ty)
        elif color == 'red':
            return (Tg + Ty, total_cycle)
        return None

    # We will maintain the set of valid T values as a list of disjoint intervals [L, R)
    # Initially, T can be any value in [0, total_cycle)
    valid_intervals = [(0, total_cycle)]

    for t, c in observations:
        # Determine the required color interval for T based on observation (t, c)
        # If light is color c at time t, then (t - T) mod total_cycle must be in the interval for c.
        # Let base_interval = get_color_interval(c)
        # We need: (t - T) % total_cycle in base_interval
        # This implies: T in (t - R, t - L] mod total_cycle (careful with open/closed)
        # Actually, let's derive strictly:
        # Let x = (t - T) % total_cycle. We need x in [L_c, R_c).
        # So L_c <= (t - T) % total_cycle < R_c
        # This is equivalent to T being in certain intervals modulo total_cycle.
        
        L_c, R_c = get_color_interval(c)
        
        # We need to find T such that (t - T) % total_cycle is in [L_c, R_c)
        # Let k be an integer. Then L_c <= t - T + k * total_cycle < R_c
        # => t - R_c + k * total_cycle < T <= t - L_c + k * total_cycle
        # So T is in (t - R_c + k*total_cycle, t - L_c + k*total_cycle]
        # Note: The original interval for x is [L_c, R_c).
        # If x = L_c, then t - T = L_c => T = t - L_c.
        # If x -> R_c, then t - T -> R_c => T -> t - R_c.
        # So T is in (t - R_c, t - L_c] modulo total_cycle.
        
        # We generate intervals for k such that the interval overlaps with [0, total_cycle)
        # The length of the interval is R_c - L_c.
        # We need to cover all possible k where the interval (t - R_c + k*C, t - L_c + k*C] intersects [0, C).
        
        new_intervals = []
        C = total_cycle
        
        # The interval is (A, B] where A = t - R_c, B = t - L_c
        # We want (A + k*C, B + k*C] intersect [0, C)
        
        # Find k such that B + k*C >= 0
        # k >= -B/C
        # Find k such that A + k*C < C
        # k < (C - A)/C
        
        # Let's just iterate k around 0. Since the interval length is < C, at most 2 intervals per period.
        # Range of k: from floor(-B/C) to ceil((C-A)/C) roughly.
        # Let's be safe and check k from -2 to 2 relative to t/C.
        
        start_k = -2
        end_k = 2
        # Adjust bounds to be safe
        # We need A + k*C < C  => k < (C - A)/C
        # We need B + k*C >= 0  => k >= -B/C
        
        # Let's compute the range of k more precisely
        # We need the intersection of (A+kC, B+kC] and [0, C) to be non-empty.
        # So max(0, A+kC) < min(C, B+kC)
        
        # Let's just generate a few candidates for k
        # t can be up to 10^9, C up to 3*10^8.
        # k roughly around -t/C.
        
        min_k = -int(t // C) - 2
        max_k = int(t // C) + 2
        
        for k in range(min_k, max_k + 1):
            A = t - R_c + k * C
            B = t - L_c + k * C
            # Interval is (A, B]
            # Intersect with [0, C)
            # Intersection is (max(A, 0), min(B, C))
            # But we must ensure max < min for non-empty intersection.
            # Also note the original interval is (A, B].
            # So intersection is (max(A, 0), min(B, C)) if max < min.
            # Wait, if B <= 0 or A >= C, no intersection.
            
            low = max(A, 0)
            high = min(B, C)
            
            if low < high:
                new_intervals.append((low, high))
        
        # Now intersect new_intervals with current valid_intervals
        if not new_intervals:
            # No valid T left
            print(0)
            return

        # Merge and intersect
        # First merge new_intervals (they should be disjoint and sorted if generated correctly, but let's sort just in case)
        new_intervals.sort()
        merged_new = []
        if new_intervals:
            curr_l, curr_r = new_intervals[0]
            for i in range(1, len(new_intervals)):
                nl, nr = new_intervals[i]
                if nl <= curr_r:
                    curr_r = max(curr_r, nr)
                else:
                    merged_new.append((curr_l, curr_r))
                    curr_l, curr_r = nl, nr
            merged_new.append((curr_l, curr_r))
        
        # Now intersect merged_new with valid_intervals
        # valid_intervals is a list of disjoint sorted intervals
        # We can do this by iterating
        
        final_intervals = []
        vi_idx = 0
        for ni in merged_new:
            ni_l, ni_r = ni
            while vi_idx < len(valid_intervals):
                vl, vr = valid_intervals[vi_idx]
                # Intersection of [ni_l, ni_r) and [vl, vr)
                # Note: our intervals are [L, R)
                inter_l = max(ni_l, vl)
                inter_r = min(ni_r, vr)
                if inter_l < inter_r:
                    final_intervals.append((inter_l, inter_r))
                vi_idx += 1
            # If we ran out of valid_intervals, we can stop? 
            # No, because merged_new might have multiple intervals and valid_intervals might have multiple.
            # But since valid_intervals is sorted and merged_new is sorted, we can optimize.
            # However, n is small (1000), so O(N^2) is fine.
            # Let's just continue checking all valid_intervals for each new interval? 
            # Actually, better to iterate through both lists.
            # Let's restart the intersection logic properly.
        
        # Re-do intersection properly
        final_intervals = []
        i = 0
        j = 0
        while i < len(valid_intervals) and j < len(merged_new):
            vl, vr = valid_intervals[i]
            nl, nr = merged_new[j]
            
            inter_l = max(vl, nl)
            inter_r = min(vr, nr)
            
            if inter_l < inter_r:
                final_intervals.append((inter_l, inter_r))
            
            if vr <= nr:
                i += 1
            else:
                j += 1
        
        valid_intervals = final_intervals
        if not valid_intervals:
            print(0)
            return

    # Now calculate the probability for the query (tq, cq)
    # We need to measure the length of T in valid_intervals such that light at tq is cq.
    # Condition: (tq - T) % total_cycle in get_color_interval(cq)
    # Same logic as before: T in (tq - R_c, tq - L_c] mod total_cycle
    
    L_q, R_q = get_color_interval(cq)
    C = total_cycle
    
    # Generate candidate intervals for T satisfying the query condition
    query_candidates = []
    min_k = -int(tq // C) - 2
    max_k = int(tq // C) + 2
    
    for k in range(min_k, max_k + 1):
        A = tq - R_q + k * C
        B = tq - L_q + k * C
        # Interval (A, B]
        low = max(A, 0)
        high = min(B, C)
        if low < high:
            query_candidates.append((low, high))
    
    if not query_candidates:
        print(0)
        return
    
    # Merge query_candidates
    query_candidates.sort()
    merged_query = []
    if query_candidates:
        curr_l, curr_r = query_candidates[0]
        for i in range(1, len(query_candidates)):
            ql, qr = query_candidates[i]
            if ql <= curr_r:
                curr_r = max(curr_r, qr)
            else:
                merged_query.append((curr_l, curr_r))
                curr_l, curr_r = ql, qr
        merged_query.append((curr_l, curr_r))
    
    # Intersect merged_query with valid_intervals
    favorable_intervals = []
    i = 0
    j = 0
    while i < len(valid_intervals) and j < len(merged_query):
        vl, vr = valid_intervals[i]
        ql, qr = merged_query[j]
        
        inter_l = max(vl, ql)
        inter_r = min(vr, qr)
        
        if inter_l < inter_r:
            favorable_intervals.append((inter_l, inter_r))
        
        if vr <= qr:
            i += 1
        else:
            j += 1
            
    if not favorable_intervals:
        print(0)
        return
    
    # Calculate total length and favorable length
    total_len = 0
    for l, r in valid_intervals:
        total_len += (r - l)
        
    favorable_len = 0
    for l, r in favorable_intervals:
        favorable_len += (r - l)
        
    if total_len == 0:
        print(0)
    else:
        print(favorable_len / total_len)

if __name__ == '__main__':
    solve()