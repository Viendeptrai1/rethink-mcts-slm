import sys
import math

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    
    x1 = int(next(iterator))
    y1 = int(next(iterator))
    x2 = int(next(iterator))
    y2 = int(next(iterator))
    
    v_max = int(next(iterator))
    t = int(next(iterator))
    
    vx = int(next(iterator))
    vy = int(next(iterator))
    
    wx = int(next(iterator))
    wy = int(next(iterator))
    
    dx = x2 - x1
    dy = y2 - y1
    dist = math.hypot(dx, dy)
    
    if dist == 0:
        print("0.0")
        return
    
    # Wind vectors
    w1 = (vx, vy)
    w2 = (wx, wy)
    
    # Magnitudes
    w1_mag = math.hypot(w1[0], w1[1])
    w2_mag = math.hypot(w2[0], w2[1])
    
    # Unit vectors for wind directions
    if w1_mag > 0:
        u1 = (w1[0] / w1_mag, w1[1] / w1_mag)
    else:
        u1 = (0.0, 0.0)
        
    if w2_mag > 0:
        u2 = (w2[0] / w2_mag, w2[1] / w2_mag)
    else:
        u2 = (0.0, 0.0)
        
    # Unit vector for destination
    if dist > 0:
        u_dest = (dx / dist, dy / dist)
    else:
        u_dest = (0.0, 0.0)
        
    # Function to calculate effective speed towards a target direction given wind vector
    # We want to maximize the component of (v_ship + wind) in the direction of u_dest
    # v_ship has magnitude v_max and direction u_ship
    # Effective velocity = v_max * u_ship + wind
    # We want to maximize dot(Effective velocity, u_dest)
    # = v_max * dot(u_ship, u_dest) + dot(wind, u_dest)
    # To maximize this, we choose u_ship such that dot(u_ship, u_dest) is maximized.
    # The maximum value of dot(u_ship, u_dest) is 1 (when u_ship == u_dest).
    # So max effective speed = v_max + dot(wind, u_dest)
    
    def get_max_speed(wind_vec, target_dir):
        # dot product of wind and target direction
        dot_wind_target = wind_vec[0] * target_dir[0] + wind_vec[1] * target_dir[1]
        return v_max + dot_wind_target

    # Check if we can reach the target in the first phase (time t)
    # If the max speed in direction of target during phase 1 is positive, we might reach it within t.
    # Actually, we need to check if the distance can be covered in time t.
    # Max speed towards target in phase 1:
    speed1 = get_max_speed(w1, u_dest)
    
    if speed1 > 0:
        time_needed_1 = dist / speed1
        if time_needed_1 <= t:
            print(f"{time_needed_1:.20f}")
            return

    # If we cannot reach in time t, we travel for time t in the optimal direction for phase 1,
    # then switch to optimal direction for phase 2.
    # Optimal direction for phase 1 is simply u_dest because the wind is constant in direction relative to the target?
    # Wait, the wind direction might not align with the target.
    # However, since we can change velocity instantly, the optimal strategy to cover distance D in time T with constant wind W is:
    # Always steer such that the velocity relative to air plus wind has the maximum projection onto the target vector.
    # This projection is maximized when the ship's velocity relative to air is aligned with the target vector.
    # Proof: Let v_s be ship velocity, |v_s| <= v_max. Let w be wind. We want to maximize (v_s + w) . u_dest.
    # = v_s . u_dest + w . u_dest.
    # Since w . u_dest is constant, we maximize v_s . u_dest. Max value is v_max when v_s is parallel to u_dest.
    # So regardless of wind direction, the optimal heading is always towards the destination.
    
    # Therefore, the strategy is:
    # 1. Fly towards destination for time t with wind w1.
    # 2. Fly towards destination for remaining time with wind w2.
    
    # Calculate distance covered in first phase
    speed1 = get_max_speed(w1, u_dest)
    # Since we know speed1 > 0 (otherwise impossible, but problem guarantees wind < v_max, so v_max + w.u >= v_max - |w| > 0)
    dist_covered_1 = speed1 * t
    
    remaining_dist = dist - dist_covered_1
    
    if remaining_dist <= 0:
        # Should have been caught by the check above, but for safety
        print(f"{t:.20f}")
        return
        
    # Calculate speed in second phase
    speed2 = get_max_speed(w2, u_dest)
    time_needed_2 = remaining_dist / speed2
    
    total_time = t + time_needed_2
    print(f"{total_time:.20f}")

if __name__ == "__main__":
    solve()