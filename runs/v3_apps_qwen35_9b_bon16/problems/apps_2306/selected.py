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
    
    # Total time
    T = sum(t)
    
    # We want to compute the maximum velocity at each second from 0 to T-1 (inclusive as integer seconds, but we'll use float for precision)
    # Let's define time points from 0.0 to T.0 with step 1.0
    # Actually, since constraints are small (T <= 100*200 = 20000), we can simulate second by second.
    
    # Let's create an array for the maximum allowed velocity at each second index i (where i goes from 0 to T-1 representing the interval [i, i+1])
    # However, velocity is continuous. The standard approach for this problem is to compute the "effective" maximum velocity profile.
    # The profile is determined by:
    # 1. The segment constraints: in segment j (duration t_j), speed <= v_j.
    # 2. The acceleration constraint: |a| <= 1.
    # 3. Start and end at 0.
    
    # We can compute the upper bound on velocity at each time point due to segment constraints.
    # Let's discretize time into integer seconds: 0, 1, 2, ..., T.
    # We need max_velocity[i] for i in 0..T.
    # Initially, based on segment constraints:
    # For a time t (integer), which segment is it in?
    # Segment j covers time range [sum(t[0]..t[j-1]), sum(t[0]..t[j])]
    # Let's define prefix sums of t.
    
    prefix_t = [0] * (N + 1)
    for i in range(N):
        prefix_t[i+1] = prefix_t[i] + t[i]
    
    # Initialize max_vel with infinity, then apply segment constraints
    # max_vel[i] = min(v_j) for all segments j that cover time i.
    # Actually, if time i is in segment j, then speed at time i must be <= v_j.
    # But wait, the constraint is "in the first t_1 seconds... speed at most v_1".
    # This applies continuously. So at any real time tau, if tau is in segment j, v(tau) <= v_j.
    # Since we discretize by integer seconds, for integer time i, we need to know which segment it belongs to.
    # Note: The boundary between segments matters.
    # Segment 0: [0, t_0]. Segment 1: [t_0, t_0+t_1], etc.
    # If i is exactly the boundary, it belongs to both? The constraint says "in the first t_1 seconds". 
    # Usually, if a time point is the end of segment j and start of j+1, it must satisfy both v_j and v_{j+1}.
    # So for integer time i, we find all segments j such that the interval [i, i] (instant) is within the segment duration.
    # Actually, simpler: For any time t, v(t) <= v_j if t is in segment j.
    # So for integer time i, we check all segments. If i is within segment j (inclusive of start, exclusive of end? or inclusive both?), 
    # we take min.
    # Let's assume inclusive for both ends of a segment's duration to be safe, or rather, the condition holds for the whole duration.
    # If duration is D, times 0, 1, ..., D-1 are strictly inside? Or 0 to D?
    # "In the first t_1 seconds" usually means [0, t_1]. So at time t_1, it is still in the first segment? 
    # And the next segment starts at t_1. So at t_1, it must satisfy both v_1 and v_2.
    
    # Let's compute initial_upper[i] for i in 0..T
    initial_upper = [float('inf')] * (T + 1)
    
    current_time = 0
    for j in range(N):
        end_time = current_time + t[j]
        speed_limit = v[j]
        # For integer times from current_time to end_time (inclusive)
        # Actually, the constraint applies to the interval [current_time, end_time].
        # Any point in time t where current_time <= t <= end_time must have v(t) <= v_j.
        # So for integer i in [current_time, end_time], initial_upper[i] = min(initial_upper[i], v_j)
        for i in range(current_time, end_time + 1):
            if i <= T:
                initial_upper[i] = min(initial_upper[i], speed_limit)
        current_time = end_time
        
    # Now propagate the acceleration constraint.
    # |v(t) - v(t-1)| <= 1. So v(t) <= v(t-1) + 1 and v(t-1) <= v(t) + 1 => v(t) >= v(t-1) - 1.
    # We want the maximum possible velocity profile.
    # Forward pass: v[i] <= v[i-1] + 1
    # Backward pass: v[i] <= v[i+1] + 1
    # Also v[0] = 0 and v[T] = 0 (must stop at start and end).
    
    # Initialize the profile with the segment constraints and boundaries.
    max_v = initial_upper[:]
    max_v[0] = 0
    max_v[T] = 0
    
    # Forward pass
    for i in range(1, T + 1):
        max_v[i] = min(max_v[i], max_v[i-1] + 1)
        
    # Backward pass
    for i in range(T - 1, -1, -1):
        max_v[i] = min(max_v[i], max_v[i+1] + 1)
        
    # Now max_v[i] is the maximum velocity allowed at integer time i.
    # However, the velocity function is continuous. Between i and i+1, the maximum velocity profile is the minimum of the line connecting (i, max_v[i]) and (i+1, max_v[i+1])?
    # No. The constraint is |a| <= 1. The function we constructed ensures that we can go from max_v[i] to max_v[i+1] with acceleration <= 1?
    # Actually, the constructed max_v array satisfies: max_v[i] <= max_v[i+1] + 1 and max_v[i+1] <= max_v[i] + 1.
    # This means |max_v[i] - max_v[i+1]| <= 1. So a constant acceleration of (max_v[i+1] - max_v[i]) works between i and i+1.
    # Is this the maximum distance?
    # Yes, because the maximum velocity at each instant is bounded by these values, and since the difference between consecutive integers is <= 1, we can achieve these velocities with acceleration exactly fitting the bound.
    # Specifically, in interval [i, i+1], if we set v(t) = max_v[i] + (t - i) * (max_v[i+1] - max_v[i]), the acceleration is constant and within [-1, 1].
    # And v(t) <= max_v[i] for t in [i, i+1]? Not necessarily.
    # Wait. The condition is that at any time t, v(t) <= constraint(t).
    # Our max_v[i] is the max velocity at integer i.
    # Does v(t) = linear interpolation satisfy v(t) <= constraint(t) for non-integer t?
    # The constraints are piecewise constant.
    # Let's re-evaluate.
    # The standard solution for this problem (ABC 179 E - "AtCoder Express 2") is exactly this:
    # 1. Determine the upper bound at each integer time point based on segment constraints.
    # 2. Apply the acceleration constraint forward and backward.
    # 3. The area under the curve formed by these points (linear interpolation) is the answer.
    # Why linear interpolation? Because between i and i+1, the max possible velocity is bounded by the lines coming from i and i+1.
    # Specifically, v(t) <= v(i) + (t-i) and v(t) <= v(i+1) - (t - (i+1)).
    # The tightest bound is min(v(i) + (t-i), v(i+1) + (i+1-t)).
    # This forms a trapezoid (or triangle) between i and i+1.
    # The area of such a trapezoid with heights h1 and h2 and width 1 is (h1 + h2) / 2.
    # So we just sum (max_v[i] + max_v[i+1]) / 2 for i from 0 to T-1.
    
    total_distance = 0.0
    for i in range(T):
        total_distance += (max_v[i] + max_v[i+1]) / 2.0
        
    print(f"{total_distance:.15f}")

if __name__ == '__main__':
    solve()