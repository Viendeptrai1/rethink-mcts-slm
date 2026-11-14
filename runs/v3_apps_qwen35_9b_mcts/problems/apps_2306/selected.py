import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return
    
    N = int(data[0])
    t = []
    v = []
    
    idx = 1
    for _ in range(N):
        t.append(int(data[idx]))
        idx += 1
    for _ in range(N):
        v.append(int(data[idx]))
        idx += 1
        
    # Calculate total time
    total_time = sum(t)
    
    # Create cumulative time boundaries to determine which segment a time step belongs to
    # cum_t[i] will be the start time of segment i (0-indexed)
    # Segment i runs from cum_t[i] to cum_t[i+1]
    cum_t = [0] * (N + 1)
    for i in range(N):
        cum_t[i+1] = cum_t[i] + t[i]
        
    # Initialize speed limit array with infinity
    # limit[i] represents the maximum speed allowed at time i (0 <= i <= total_time)
    limit = [float('inf')] * (total_time + 1)
    
    # Set boundary conditions: start and end must be 0
    limit[0] = 0.0
    limit[total_time] = 0.0
    
    # Forward pass
    # Propagate constraints from t=0 to t=total_time
    # For each second, speed can increase by at most 1, but cannot exceed the segment limit
    current_seg = 0
    for i in range(1, total_time + 1):
        # Determine which segment this time step belongs to
        # The interval (i-1, i] belongs to segment k if cum_t[k] <= i-1 and i <= cum_t[k+1]
        # Since we iterate i from 1 upwards, we can track the segment
        while current_seg < N and cum_t[current_seg + 1] < i:
            current_seg += 1
        
        # The speed limit for this segment is v[current_seg]
        seg_limit = v[current_seg]
        
        # Update limit based on previous time step and segment constraint
        limit[i] = min(limit[i], limit[i-1] + 1.0, float(seg_limit))
        
    # Backward pass
    # Propagate constraints from t=total_time to t=0
    # For each second, speed can decrease by at most 1 (in reverse, increase by 1 going backwards)
    # but cannot exceed the segment limit
    current_seg = N - 1
    for i in range(total_time - 1, -1, -1):
        # Determine which segment this time step belongs to
        while current_seg >= 0 and cum_t[current_seg + 1] <= i:
            current_seg -= 1
            
        seg_limit = v[current_seg]
        
        # Update limit based on next time step and segment constraint
        limit[i] = min(limit[i], limit[i+1] + 1.0, float(seg_limit))
        
    # Calculate total distance
    # Distance = integral of speed over time
    # Since speed changes by at most 1 per second, we can approximate by summing speeds at each second
    # However, to be precise with the continuous nature, we consider the trapezoidal rule or simply summing
    # the area under the curve defined by the max speed profile.
    # The max speed profile is piecewise linear with slopes of +1, 0, or -1.
    # The distance is the sum of (limit[i] + limit[i+1]) / 2 for each interval [i, i+1]
    
    total_distance = 0.0
    for i in range(total_time):
        total_distance += (limit[i] + limit[i+1]) / 2.0
        
    print(f"{total_distance:.15f}")

if __name__ == '__main__':
    solve()