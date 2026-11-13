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
            t_obs = int(next(iterator))
            color_str = next(iterator)
            observations.append((t_obs, color_str))
        
        t_q = int(next(iterator))
        c_q = next(iterator)
        
    except StopIteration:
        return

    # Cycle parameters
    # Green: [0, Tg)
    # Yellow: [Tg, Tg + Ty)
    # Red: [Tg + Ty, Tg + Ty + Tr)
    
    total_cycle = Tg + Ty + Tr
    
    # Convert colors to canonical names to handle case insensitivity if needed, 
    # though problem implies exact match. We'll use lower() for safety.
    def get_color_range(color):
        if color == 'green':
            return (0, Tg)
        elif color == 'yellow':
            return (Tg, Tg + Ty)
        elif color == 'red':
            return (Tg + Ty, Tg + Ty + Tr)
        return (0, 0)

    # Valid intervals for T modulo total_cycle
    # An observation (t, c) is valid if:
    # floor((t - T) / total_cycle) * total_cycle + (t - T) % total_cycle falls in the range for c.
    # Actually simpler: Let offset = T % total_cycle.
    # The phase at time t is (t - offset) % total_cycle.
    # This phase must be in the valid range for color c.
    # So: range_start <= (t - offset) % total_cycle < range_end
    # Let x = offset. We need: range_start <= (t - x) % total_cycle < range_end
    
    # This inequality defines valid x modulo total_cycle.
    # Let's solve for x in [0, total_cycle).
    # (t - x) % total_cycle = y, where y is in [L, R)
    # This means t - x = k * total_cycle + y for some integer k.
    # x = t - k * total_cycle - y
    # x = t - y (mod total_cycle)
    # So x must be in [t - R + 1, t - L] modulo total_cycle? 
    # Let's re-derive carefully.
    # Condition: L <= (t - x) % total_cycle < R
    # Let val = (t - x) % total_cycle. Then val in [L, R).
    # Also val = (t - x) if t >= x, else t - x + total_cycle.
    # Case 1: t >= x. Then L <= t - x < R  =>  t - R < x <= t - L.
    # Case 2: t < x. Then L <= t - x + total_cycle < R  =>  t - R + total_cycle < x <= t - L + total_cycle.
    # Combined, x must be in intervals:
    # I1 = (t - R, t - L]  (if we consider real numbers, but x is integer? T is real? Problem says integers, but T is unknown real? 
    # Wait, "fixed green-yellow-red cycle... how long each stage lasts". Usually implies integer seconds if inputs are integers.
    # However, T could be any real number? "deduce what values of T are (im)possible".
    # If T is real, the valid set for T mod total_cycle is a union of intervals.
    # Since we need probability, we deal with lengths of these intervals.
    
    # Let's define the valid set of phases phi = T % total_cycle.
    # phi is a real number in [0, total_cycle).
    # Condition: L <= (t - phi) % total_cycle < R
    # Let u = (t - phi) % total_cycle. u is in [L, R).
    # Then phi = t - u (mod total_cycle).
    # As u ranges over [L, R), phi ranges over [t - R, t - L] modulo total_cycle.
    # The length of this interval for phi is R - L.
    # So each observation restricts phi to a set of intervals within [0, total_cycle) with total length equal to the duration of the color in the cycle.
    
    # Let valid_phi be a list of disjoint intervals [a, b) within [0, total_cycle) that satisfy all observations.
    # Initially, valid_phi = [(0, total_cycle)]
    
    # For each observation (t, c):
    #   L, R = get_color_range(c)
    #   # We need to intersect current valid_phi with the set of phi such that (t - phi)%total_cycle in [L, R)
    #   # The set of such phi is: S = { phi in [0, total_cycle) | (t - phi)%total_cycle in [L, R) }
    #   # S is the union of intervals:
    #   # Interval 1: from t - R to t - L (shifted to be positive)
    #   # Let's compute the base interval for phi: [t - R, t - L]
    #   # We need to wrap this interval modulo total_cycle.
    
    # Let's implement interval intersection.
    
    valid_intervals = [(0.0, float(total_cycle))]
    
    for t_obs, color in observations:
        L, R = get_color_range(color)
        if L >= R:
            continue
            
        # Determine the valid phi intervals for this observation
        # Condition: L <= (t_obs - phi) % total_cycle < R
        # Let delta = (t_obs - phi) % total_cycle. Then delta in [L, R).
        # phi = (t_obs - delta) % total_cycle.
        # As delta goes from L to R, phi goes from (t_obs - R) to (t_obs - L) modulo total_cycle.
        # The length of the valid phi region is R - L.
        
        # The raw interval for phi is [t_obs - R, t_obs - L].
        # We need to normalize this to [0, total_cycle) by wrapping.
        
        low_raw = t_obs - R
        high_raw = t_obs - L
        
        # We can decompose [low_raw, high_raw] into segments modulo total_cycle.
        # Since high_raw - low_raw = R - L < total_cycle (as R <= total_cycle, L >= 0),
        # there is at most one wrap-around or just one continuous segment if no wrap, 
        # or two segments if it crosses the boundary.
        # Actually, since the length is less than total_cycle, the set of valid phi is a single connected arc on the circle.
        # It will appear as either [a, b) or [a, total_cycle) U [0, b) if it wraps.
        
        # Let's shift the interval so low_raw is >= 0 by adding multiples of total_cycle?
        # Easier: define start = low_raw, end = high_raw.
        # Normalize start to [0, total_cycle): s = start % total_cycle
        # The interval covers length (R-L).
        # If end > start (no wrap in raw logic relative to period?), wait.
        # Let's just generate the intervals by taking the raw interval and mapping modulo total_cycle.
        
        # The raw interval is I = [low_raw, high_raw].
        # We want { x % total_cycle | x in I }.
        # Since length(I) < total_cycle, this is either:
        # 1. If floor(high_raw/total_cycle) == floor(low_raw/total_cycle): just [s, e') where e' is normalized end.
        # 2. If floor(high_raw/total_cycle) > floor(low_raw/total_cycle): splits into [s, total_cycle) and [0, e').
        
        # Calculate normalized start and end
        s = low_raw % total_cycle
        e_raw = high_raw
        
        # Determine the end in the normalized frame
        # If e_raw < s + total_cycle? Not necessarily.
        # Let's find the number of full cycles.
        # The interval starts at s and has length len = R - L.
        # It ends at s + len.
        # If s + len < total_cycle: interval is [s, s + len)
        # If s + len >= total_cycle: interval is [s, total_cycle) U [0, s + len - total_cycle)
        
        length = R - L
        end_pos = s + length
        
        if end_pos <= total_cycle:
            new_intervals = [(s, end_pos)]
        else:
            new_intervals = [(s, total_cycle), (0, end_pos - total_cycle)]
        
        # Now intersect new_intervals with valid_intervals
        next_valid = []
        
        for v_start, v_end in valid_intervals:
            for n_start, n_end in new_intervals:
                # Intersection of [v_start, v_end) and [n_start, n_end)
                inter_start = max(v_start, n_start)
                inter_end = min(v_end, n_end)
                if inter_start < inter_end:
                    next_valid.append((inter_start, inter_end))
        
        valid_intervals = next_valid
        
        # If no valid intervals left, probability is 0
        if not valid_intervals:
            # But we need to handle the query. If impossible, prob is 0.
            # We can stop early? Yes, but let's finish loop to be safe, though it won't change.
            pass

    # Calculate total measure
    total_measure = 0.0
    for s, e in valid_intervals:
        total_measure += (e - s)
    
    if total_measure <= 1e-9:
        print(0.0)
        return

    # Query: probability of color c_q at time t_q
    # We need the measure of phi in valid_intervals such that (t_q - phi) % total_cycle is in get_color_range(c_q)
    # Let Lq, Rq = get_color_range(c_q)
    # Condition: Lq <= (t_q - phi) % total_cycle < Rq
    # This is equivalent to phi being in the set S_q defined similarly to above for t_q.
    
    Lq, Rq = get_color_range(c_q)
    length_q = Rq - Lq
    
    s_q = (t_q - Rq) % total_cycle # Wait, derivation:
    # We want phi such that (t_q - phi)%T in [Lq, Rq)
    # phi = (t_q - delta)%T where delta in [Lq, Rq)
    # So phi ranges from (t_q - Rq) to (t_q - Lq) mod T.
    # Start of phi interval s_q = (t_q - Rq) % total_cycle
    # Length of phi interval = Rq - Lq
    
    s_q = (t_q - Rq) % total_cycle
    end_pos_q = s_q + length_q
    
    favorable_measure = 0.0
    
    # Check intersection of valid_intervals with the query interval(s)
    if length_q > 0:
        if end_pos_q <= total_cycle:
            query_intervals = [(s_q, end_pos_q)]
        else:
            query_intervals = [(s_q, total_cycle), (0, end_pos_q - total_cycle)]
        
        for v_start, v_end in valid_intervals:
            for q_start, q_end in query_intervals:
                inter_start = max(v_start, q_start)
                inter_end = min(v_end, q_end)
                if inter_start < inter_end:
                    favorable_measure += (inter_end - inter_start)
    
    if total_measure == 0:
        print(0.0)
    else:
        print(favorable_measure / total_measure)

if __name__ == '__main__':
    solve()