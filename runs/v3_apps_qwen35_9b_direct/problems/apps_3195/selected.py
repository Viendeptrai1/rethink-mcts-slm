import sys
import math

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
            color = next(iterator)
            observations.append((t_obs, color))
        
        t_q = int(next(iterator))
        c_q = next(iterator)
        
    except StopIteration:
        return

    # Total cycle length
    T_cycle = Tg + Ty + Tr

    # We need to find the set of possible start times T (mod T_cycle)
    # such that all observations are consistent.
    # Let the cycle start at time T (0 <= T < T_cycle).
    # At any absolute time t, the phase is (t - T) mod T_cycle.
    # The color depends on this phase:
    # [0, Tg) -> Green
    # [Tg, Tg+Ty) -> Yellow
    # [Tg+Ty, T_cycle) -> Red

    # For each observation (t, c), we can determine the valid range of phases [0, T_cycle)
    # that would result in color c.
    # Then, for a fixed T, the phase at time t is (t - T) mod T_cycle.
    # So we need: phase_in_color_range((t - T) mod T_cycle) is True.
    # This is equivalent to: (t - T) mod T_cycle must be in the valid phase interval for color c.
    # Let valid_phase_interval be [start_c, end_c).
    # We need: start_c <= (t - T) mod T_cycle < end_c.
    # Let x = (t - T) mod T_cycle. Then x = (t - T) + k*T_cycle for some integer k.
    # So start_c <= t - T + k*T_cycle < end_c
    # => start_c - t + k*T_cycle <= -T < end_c - t + k*T_cycle
    # => t - end_c + k*T_cycle < T <= t - start_c + k*T_cycle
    # This gives a set of intervals for T modulo T_cycle.

    # Define phase intervals for each color:
    # Green: [0, Tg)
    # Yellow: [Tg, Tg+Ty)
    # Red: [Tg+Ty, T_cycle)

    def get_phase_interval(color):
        if color == 'green':
            return (0, Tg)
        elif color == 'yellow':
            return (Tg, Tg + Ty)
        elif color == 'red':
            return (Tg + Ty, T_cycle)
        else:
            return None

    # For each observation, compute the valid intervals for T in [0, T_cycle)
    # An observation (t, c) with phase interval [s, e) implies:
    # s <= (t - T) mod T_cycle < e
    # This splits into cases based on k such that t - T + k*T_cycle is in [s, e).
    # T must be in (t - e + k*T_cycle, t - s + k*T_cycle]
    # We are interested in T mod T_cycle, so we can consider k such that the interval overlaps [0, T_cycle).
    
    valid_T_intervals = [] # List of (start, end) representing valid T ranges within [0, T_cycle)

    for t_obs, color in observations:
        s, e = get_phase_interval(color)
        if s is None:
            continue
        
        # We need s <= (t_obs - T) mod T_cycle < e
        # Let val = t_obs - T. We need val mod T_cycle in [s, e).
        # This means there exists integer k such that:
        # s <= val + k*T_cycle < e
        # s <= t_obs - T + k*T_cycle < e
        # T <= t_obs - s + k*T_cycle  AND  T > t_obs - e + k*T_cycle
        # So T in (t_obs - e + k*T_cycle, t_obs - s + k*T_cycle]
        
        # We want to find all such intervals that intersect [0, T_cycle).
        # The length of the interval is (t_obs - s + k*T_cycle) - (t_obs - e + k*T_cycle) = e - s.
        # Since e - s <= T_cycle, the interval length is at most T_cycle.
        
        # We can iterate k such that the interval overlaps [0, T_cycle).
        # The interval is (L, R] where L = t_obs - e + k*T_cycle, R = t_obs - s + k*T_cycle.
        # We need max(0, L) < T <= min(T_cycle, R).
        # Overlap exists if L < R (always true since s < e) and the interval [0, T_cycle) intersects (L, R].
        # Intersection is non-empty if L < T_cycle and R > 0.
        
        # Find range of k:
        # L < T_cycle => t_obs - e + k*T_cycle < T_cycle => k*T_cycle < T_cycle - t_obs + e => k < 1 + (T_cycle - t_obs + e)/T_cycle
        # R > 0 => t_obs - s + k*T_cycle > 0 => k*T_cycle > s - t_obs => k > (s - t_obs)/T_cycle
        
        # Since t_obs can be large, we compute k_min and k_max carefully.
        # k_min = floor((s - t_obs) / T_cycle) + 1  (since strict inequality for lower bound of k)
        # Actually: k > (s - t_obs)/T_cycle. So k_min = floor((s - t_obs)/T_cycle) + 1.
        # k_max: k < 1 + (T_cycle - t_obs + e)/T_cycle. So k_max = ceil(1 + (T_cycle - t_obs + e)/T_cycle) - 1?
        # Let's just use integer arithmetic.
        # Condition: t_obs - e + k*T_cycle < T_cycle  => k*T_cycle < T_cycle - t_obs + e
        # If T_cycle - t_obs + e <= 0, then no k satisfies this? No, k can be negative.
        # k < (T_cycle - t_obs + e) / T_cycle.
        # k_max = floor((T_cycle - t_obs + e - 1) / T_cycle) if numerator >= 0 else ...
        # Actually simpler: iterate k around 0.
        # The interval for T is periodic with T_cycle. We only care about T in [0, T_cycle).
        # The condition is equivalent to: (t_obs - T) mod T_cycle in [s, e).
        # Let's shift the problem: Let T' = T mod T_cycle.
        # We need s <= (t_obs - T') mod T_cycle < e.
        # This is a standard modular interval problem.
        # The set of T' in [0, T_cycle) satisfying this is a union of at most 2 intervals.
        # Specifically, let offset = t_obs mod T_cycle.
        # We need s <= (offset - T') mod T_cycle < e.
        # Let x = (offset - T') mod T_cycle.
        # If offset >= s:
        #   Case 1: offset - T' in [s, e) => T' in (offset - e, offset - s]
        #   Case 2: offset - T' + T_cycle in [s, e) => T' in (offset - e + T_cycle, offset - s + T_cycle] -> but T' < T_cycle, so this might be empty or wrap.
        # Actually, let's just compute the valid T' directly.
        # We want T' such that (offset - T') % T_cycle in [s, e).
        # Let y = (offset - T') % T_cycle.
        # y = offset - T' if offset >= T'
        # y = offset - T' + T_cycle if offset < T'
        
        # Case A: offset >= T'. Then y = offset - T'.
        # s <= offset - T' < e  =>  offset - e < T' <= offset - s.
        # Also T' <= offset (from assumption).
        # So T' in (max(0, offset - e), min(offset, offset - s)].
        # Note: offset - s <= offset, so min is offset - s.
        # Interval A: (max(0, offset - e), offset - s]
        
        # Case B: offset < T'. Then y = offset - T' + T_cycle.
        # s <= offset - T' + T_cycle < e  =>  s - offset - T_cycle <= -T' < e - offset - T_cycle
        # => offset + T_cycle - e < T' <= offset + T_cycle - s.
        # Also T' > offset (from assumption).
        # So T' in (max(offset, offset + T_cycle - e), offset + T_cycle - s].
        # Note: offset + T_cycle - e > offset (since e <= T_cycle).
        # So lower bound is offset + T_cycle - e.
        # Interval B: (offset + T_cycle - e, offset + T_cycle - s]
        
        # Combine these two intervals, intersecting with [0, T_cycle).
        # Since offset < T_cycle, offset - s might be negative.
        # Interval A: (max(0, offset - e), offset - s] intersected with [0, T_cycle).
        # Since offset - s <= offset < T_cycle, the upper bound is fine.
        # Lower bound: max(0, offset - e).
        # Valid if max(0, offset - e) < offset - s.
        
        # Interval B: (offset + T_cycle - e, offset + T_cycle - s] intersected with [0, T_cycle).
        # Lower bound: offset + T_cycle - e. Since e > 0, this is < offset + T_cycle.
        # Upper bound: offset + T_cycle - s. Since s >= 0, this is <= offset + T_cycle.
        # We need to intersect with [0, T_cycle).
        # Lower bound might be >= T_cycle? 
        # offset + T_cycle - e < T_cycle + T_cycle - e. Could be >= T_cycle if e is small?
        # offset < T_cycle, so offset + T_cycle - e < 2*T_cycle - e.
        # If e is small, offset + T_cycle - e could be > T_cycle.
        # But we need T' < T_cycle.
        # So we take min(T_cycle, upper_bound).
        # Also lower bound must be < upper bound.
        
        offset = t_obs % T_cycle
        
        # Interval A
        low_A = max(0, offset - e)
        high_A = offset - s
        if low_A < high_A:
            # Intersect with [0, T_cycle) -> high_A is already < T_cycle
            valid_T_intervals.append((low_A, high_A))
        
        # Interval B
        low_B = offset + T_cycle - e
        high_B = offset + T_cycle - s
        # Intersect with [0, T_cycle)
        # low_B could be >= T_cycle? 
        # offset < T_cycle, e > 0 => offset + T_cycle - e < T_cycle + T_cycle.
        # If e is very small, low_B could be > T_cycle.
        # We need low_B < T_cycle for any overlap.
        # Also high_B could be >= T_cycle.
        
        real_low_B = low_B
        real_high_B = high_B
        
        if real_low_B < T_cycle:
            real_high_B = min(real_high_B, T_cycle)
            if real_low_B < real_high_B:
                valid_T_intervals.append((real_low_B, real_high_B))

    # Now we have a list of intervals (start, end) for T in [0, T_cycle).
    # We need to merge overlapping intervals.
    if not valid_T_intervals:
        # No possible T? But problem says observations are consistent with some T?
        # Or maybe no T satisfies all? Then probability is 0.
        total_valid = 0
    else:
        valid_T_intervals.sort()
        merged = []
        if valid_T_intervals:
            curr_start, curr_end = valid_T_intervals[0]
            for i in range(1, len(valid_T_intervals)):
                s, e = valid_T_intervals[i]
                if s <= curr_end:
                    curr_end = max(curr_end, e)
                else:
                    merged.append((curr_start, curr_end))
                    curr_start, curr_end = s, e
            merged.append((curr_start, curr_end))
        
        total_valid = sum(e - s for s, e in merged)
        if total_valid <= 0:
            total_valid = 0

    if total_valid == 0:
        print(f"{0.0:.10f}")
        return

    # Now compute the probability for the query (t_q, c_q)
    # We need to count how many T in the valid set result in color c_q at time t_q.
    # Similar logic: find valid T intervals for the query, intersect with merged valid intervals.
    
    s_q, e_q = get_phase_interval(c_q)
    if s_q is None:
        # Should not happen based on problem statement
        print(f"{0.0:.10f}")
        return

    offset_q = t_q % T_cycle
    
    # Compute valid T intervals for the query
    query_intervals = []
    
    # Case A: offset_q >= T'
    low_A = max(0, offset_q - e_q)
    high_A = offset_q - s_q
    if low_A < high_A:
        query_intervals.append((low_A, high_A))
    
    # Case B: offset_q < T'
    low_B = offset_q + T_cycle - e_q
    high_B = offset_q + T_cycle - s_q
    if low_B < T_cycle:
        real_high_B = min(high_B, T_cycle)
        if low_B < real_high_B:
            query_intervals.append((low_B, real_high_B))
    
    # Intersect query_intervals with merged valid intervals
    favorable = 0.0
    
    # Sort query intervals
    query_intervals.sort()
    
    # For each merged valid interval, intersect with each query interval
    for (vs, ve) in merged:
        for (qs, qe) in query_intervals:
            # Intersection of [vs, ve) and [qs, qe)
            inter_start = max(vs, qs)
            inter_end = min(ve, qe)
            if inter_start < inter_end:
                favorable += (inter_end - inter_start)
    
    if favorable == 0:
        print(f"{0.0:.10f}")
    else:
        prob = favorable / total_valid
        print(f"{prob:.10f}")

if __name__ == "__main__":
    solve()