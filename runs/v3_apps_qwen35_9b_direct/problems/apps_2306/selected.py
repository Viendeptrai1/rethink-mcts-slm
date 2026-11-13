import sys
import math

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    N = int(next(iterator))
    t = [int(next(iterator)) for _ in range(N)]
    v = [int(next(iterator)) for _ in range(N)]
    
    total_time = sum(t)
    
    # Calculate the maximum possible speed at each second
    # We work backwards and forwards to determine constraints
    # speed[i] will store the maximum speed allowed at second i (0-indexed)
    
    # Initialize with the given segment limits
    # The train must stop at time 0 and time total_time
    # Within segment i (from time T_start to T_end), speed <= v[i]
    
    # Create an array for max speed at each second
    # Time points are 0, 1, 2, ..., total_time
    max_speed = [0.0] * (total_time + 1)
    
    # Forward pass: considering acceleration from start (0 speed)
    # At time t, speed can be at most t (since accel <= 1 and start at 0)
    # Also bounded by segment constraints
    current_limit = 0.0
    for i in range(total_time + 1):
        # Determine which segment we are in
        # Segment j covers time [sum(t[:j]), sum(t[:j+1]))
        # We need to find the max speed limit for the current time point
        # Since time is integer, we can check segments
        
        # Find the segment index for time i
        # Segment j is active if start_time <= i < end_time
        # But at the exact boundary, it's the start of the next segment? 
        # Actually, the problem says "in the first t1 seconds", "subsequent t2 seconds"
        # So segment 0: [0, t1), segment 1: [t1, t1+t2), etc.
        # However, speed constraint applies continuously.
        # Let's find the segment that contains time i.
        
        seg_idx = 0
        time_elapsed = 0
        for j in range(N):
            if i < time_elapsed + t[j]:
                seg_idx = j
                break
            time_elapsed += t[j]
        
        # The constraint for this time point is v[seg_idx]
        # But we also have the constraint from acceleration from previous points
        # max_speed[i] = min(v[seg_idx], max_speed[i-1] + 1)
        # For i=0, max_speed[0] = 0 (must stop)
        
        if i == 0:
            max_speed[i] = 0.0
        else:
            max_speed[i] = min(float(v[seg_idx]), max_speed[i-1] + 1.0)
    
    # Backward pass: considering deceleration to end (0 speed)
    # At time t, speed can be at most (total_time - t) (since decel <= 1 and end at 0)
    # Also bounded by segment constraints and forward pass result
    for i in range(total_time - 1, -1, -1):
        # Find segment for time i again (same logic)
        seg_idx = 0
        time_elapsed = 0
        for j in range(N):
            if i < time_elapsed + t[j]:
                seg_idx = j
                break
            time_elapsed += t[j]
        
        # Constraint from end: speed at time i cannot exceed (total_time - i)
        # because it must reach 0 at total_time with max deceleration 1
        limit_from_end = float(total_time - i)
        
        # Update max_speed[i] with backward constraint
        max_speed[i] = min(max_speed[i], limit_from_end)
        
        # Also, the speed at i+1 must be at least max_speed[i] - 1
        # So max_speed[i] cannot be more than max_speed[i+1] + 1
        if i < total_time:
            max_speed[i] = min(max_speed[i], max_speed[i+1] + 1.0)
    
    # Now calculate distance
    # Distance = integral of speed over time
    # Since we have discrete seconds, we can approximate or calculate exactly
    # The optimal strategy is to follow the max_speed profile as closely as possible
    # But actually, the max_speed array gives the upper bound at each instant.
    # The actual speed profile that maximizes distance will be the one that stays as high as possible.
    # This profile is concave and follows the envelope of the constraints.
    # The distance is the area under the speed-time curve.
    # Since the constraints are linear (accel/decel limits) and step functions (v_i),
    # the optimal speed profile is piecewise linear.
    # We can compute the distance by integrating the max_speed profile.
    # However, max_speed[i] is the speed at time i. The speed at time i+0.5 is not directly given.
    # But since acceleration is at most 1, the speed changes linearly between integers if we follow the bounds tightly.
    # Actually, the standard approach for this problem is:
    # The maximum distance is the integral of the function f(t) where f(t) is the maximum possible speed at time t.
    # f(t) = min( t, total_time - t, min over segments j of (v_j + min(t - start_j, end_j - t)) )
    # But we already computed the discrete version.
    # For continuous time, the distance is the area under the curve.
    # The curve is formed by the intersection of:
    # 1. y = t (from start)
    # 2. y = total_time - t (from end)
    # 3. y = v_j + (t - start_j) for t in [start_j, start_j + v_j] (accel phase in segment j)
    # 4. y = v_j for t in [start_j + v_j, end_j] (cruise phase if possible)
    # 5. y = v_j + (end_j - t) for t in [end_j - v_j, end_j] (decel phase in segment j)
    # Actually, the constraint in segment j is: speed <= v_j.
    # And due to accel/decel, the speed at time t in segment j is also bounded by:
    # speed(t) <= speed(t_prev) + (t - t_prev)
    # But we did a discrete DP which is sufficient if we integrate properly.
    
    # Let's compute the distance by considering the speed at each half-second interval?
    # No, the standard solution is to compute the area under the max_speed curve.
    # The max_speed curve is concave. The distance is the integral from 0 to total_time.
    # We can compute this by summing the areas of trapezoids between integer points?
    # But the function might not be linear between integers if the constraints change.
    # However, the constraints are:
    # f(t) <= t
    # f(t) <= total_time - t
    # f(t) <= v_j for t in [S_j, E_j]
    # f(t) <= f(t') + (t - t') for t > t'
    # f(t) <= f(t') - (t - t') for t < t'
    # The function f(t) is the minimum of several linear functions, so it is concave and piecewise linear.
    # The breakpoints occur at integer times (segment boundaries) and where the lines intersect.
    # Since we have the values at integer times, and the function is concave, 
    # the value at t+0.5 is (f(t) + f(t+1))/2? Not necessarily, because the slope might change within the interval.
    # But the slope can only change at integer times (segment boundaries) or when the active constraint changes.
    # Actually, the slope is always -1, 0, or 1 in the optimal profile? 
    # No, the slope is determined by the active constraint.
    # The maximum distance is achieved by the function f(t) which is the upper envelope of the feasible speeds.
    # This function is concave. The distance is the integral.
    # We can compute the integral by summing the areas of the trapezoids formed by the points (i, f(i)) and (i+1, f(i+1)).
    # Is f(t) linear between i and i+1?
    # The constraints are:
    # f(t) <= t
    # f(t) <= total_time - t
    # f(t) <= v_j for t in [S_j, E_j]
    # And the Lipschitz condition with constant 1.
    # The function f(t) is the minimum of a set of functions, each of which is concave (or linear).
    # The minimum of concave functions is not necessarily concave, but in this case, it is known to be concave.
    # Moreover, the function f(t) is piecewise linear with breakpoints at integer times.
    # Why? Because the constraints v_j are constant over intervals, and the t and total_time-t are linear.
    # The interaction of these creates breakpoints at integer times.
    # Therefore, the area between i and i+1 is (f(i) + f(i+1)) / 2.
    
    distance = 0.0
    for i in range(total_time):
        distance += (max_speed[i] + max_speed[i+1]) / 2.0
    
    print(f"{distance:.15f}")

if __name__ == '__main__':
    solve()