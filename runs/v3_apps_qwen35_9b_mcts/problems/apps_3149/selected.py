import sys
import math

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        n = int(next(iterator))
        omega = float(next(iterator))
        v0 = float(next(iterator))
        theta_deg = int(next(iterator))
        w = float(next(iterator))
        
        vertices = []
        for _ in range(n):
            x = float(next(iterator))
            y = float(next(iterator))
            vertices.append((x, y))
    except StopIteration:
        return

    # Convert initial angle to radians
    # Angle is measured counter-clockwise relative to (1, 0)
    theta_rad = math.radians(theta_deg)

    # Initial velocity components
    vx0 = v0 * math.cos(theta_rad)
    vy0 = v0 * math.sin(theta_rad)

    # Gravity
    g = 9.81

    # Wall x-coordinate
    wall_x = w

    # We need to find the time T for each vertex to hit the wall (x = wall_x)
    # The cookie rotates clockwise with angular velocity omega.
    # Initial angle of the cookie is not explicitly given as a rotation angle, 
    # but the problem says "initial angle" for trajectory and then gives vertices.
    # Usually in such problems, the vertices are given in the cookie's local frame 
    # aligned with the world frame at t=0, or we assume the vertices are world coordinates at t=0.
    # The problem states: "Each line contains ... denoting the initial position of a cookie's corner."
    # So vertices are world coordinates at t=0.
    # The rotation applies to the orientation of the cookie as it flies.
    # However, the position of the center of mass follows a parabola.
    # We need the center of mass (COM) first.

    # Calculate Center of Mass (assuming uniform density, centroid of polygon)
    # Since vertices are in CCW order, we can use the standard polygon centroid formula.
    cx = 0.0
    cy = 0.0
    area = 0.0
    sum_x = 0.0
    sum_y = 0.0

    for i in range(n):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % n]
        cross = x1 * y2 - x2 * y1
        area += cross
        sum_x += (x1 + x2) * cross
        sum_y += (y1 + y2) * cross

    area *= 0.5
    if area == 0:
        # Should not happen based on problem statement
        return

    cx = sum_x / (6.0 * area)
    cy = sum_y / (6.0 * area)

    # Now, for each vertex, we need to track its position over time.
    # The vertex position at time t is:
    # P(t) = COM(t) + R(-omega * t) * (P0 - COM)
    # where R is the rotation matrix for clockwise rotation by angle alpha = omega * t.
    # Clockwise rotation by alpha is equivalent to counter-clockwise by -alpha.
    # Rotation matrix for angle phi (CCW):
    # [ cos(phi)  -sin(phi) ]
    # [ sin(phi)   cos(phi)  ]
    # Here phi = -omega * t.
    # cos(-alpha) = cos(alpha), sin(-alpha) = -sin(alpha).
    # So:
    # x_rel(t) = (x0 - cx) * cos(omega*t) - (y0 - cy) * (-sin(omega*t))
    #          = (x0 - cx) * cos(omega*t) + (y0 - cy) * sin(omega*t)
    # y_rel(t) = (x0 - cx) * (-sin(omega*t)) + (y0 - cy) * cos(omega*t)
    #          = -(x0 - cx) * sin(omega*t) + (y0 - cy) * cos(omega*t)

    # COM trajectory:
    # cx(t) = cx + vx0 * t
    # cy(t) = cy + vy0 * t - 0.5 * g * t^2

    # We need to find t > 0 such that x_vertex(t) = wall_x.
    # x_vertex(t) = cx(t) + x_rel(t)
    # wall_x = cx + vx0 * t + (x0 - cx) * cos(omega*t) + (y0 - cy) * sin(omega*t)
    # Let dx0 = x0 - cx, dy0 = y0 - cy.
    # wall_x - cx = vx0 * t + dx0 * cos(omega*t) + dy0 * sin(omega*t)
    # Let target = wall_x - cx.
    # f(t) = vx0 * t + dx0 * cos(omega*t) + dy0 * sin(omega*t) - target = 0

    # We will solve this equation for each vertex using binary search or Newton's method.
    # Given the constraints and nature of the function, binary search is robust if we can find bounds.
    # However, the function is oscillatory if omega is large. But omega <= 10.
    # The cookie hits the wall "first". We assume the first hit is the global minimum positive t.
    # Since the cookie is thrown towards the wall (vx0 > 0 usually, unless angle is weird),
    # and wall_x > initial x (implied by "moving towards"), we expect a solution.
    # Note: vx0 could be negative if angle > 90, but problem says "moving towards the wall".
    # Let's assume vx0 > 0. If vx0 <= 0, it might never hit or hit later after bouncing? 
    # Problem says "moving towards", so vx0 should be positive.
    
    # Let's define the function for a specific vertex
    def get_x_at_time(t, x0, y0):
        # COM at time t
        com_x = cx + vx0 * t
        # Relative position rotated
        angle = omega * t
        dx = x0 - cx
        dy = y0 - cy
        # Clockwise rotation of vector (dx, dy) by angle
        # x' = dx * cos(a) + dy * sin(a)
        # y' = -dx * sin(a) + dy * cos(a)
        rx = dx * math.cos(angle) + dy * math.sin(angle)
        return com_x + rx

    # We need to find the smallest t > 0 for any vertex such that get_x_at_time(t, x0, y0) == wall_x.
    # Since the function is continuous and we expect the first hit to be relatively soon,
    # we can search in a range [0, T_max]. What is a safe T_max?
    # Max distance is roughly 40 (coords < 20). Min vx is 1. Max time ~ 40s.
    # But with gravity, it could be longer. Let's use a generous upper bound like 1000s.
    # However, if vx0 is small and gravity pulls it down, it might take long.
    # Let's try to find the root for each vertex and pick the minimum positive one.

    best_vertex_idx = -1
    best_time = float('inf')

    for i in range(n):
        x0, y0 = vertices[i]
        
        # Define function f(t) = get_x_at_time(t) - wall_x
        # We want f(t) = 0
        
        # Check if it's possible to hit the wall.
        # If vx0 <= 0, it moves away or parallel. But problem implies it hits.
        # Let's assume vx0 > 0.
        
        # We can use binary search to find the first time it crosses wall_x.
        # But the function oscillates. We want the FIRST crossing.
        # Since at t=0, x = x0. If x0 < wall_x, and vx0 > 0, it will cross.
        # If x0 > wall_x, it might have already passed or is moving away.
        # Given "moving towards", likely x0 < wall_x.
        
        if x0 >= wall_x:
            # If starting at or beyond wall, and moving towards (vx0 > 0), it's already past?
            # Or maybe vx0 < 0? But "moving towards" implies direction.
            # Let's assume standard case: x0 < wall_x.
            # If x0 >= wall_x, skip or handle carefully. 
            # If x0 == wall_x, t=0 is a hit? But we need t > 0? 
            # Problem says "hits the wall first". Usually implies future.
            # If it starts on the wall, maybe t=0? But let's assume x0 < wall_x.
            continue

        # Binary search for the first root
        low = 0.0
        high = 1000.0 # Generous upper bound
        
        # Check if f(high) is still negative (meaning it hasn't crossed yet or oscillated back)
        # Actually, with gravity, x doesn't change much due to y, only vx0 matters for x trend.
        # x(t) = cx + vx0*t + ...
        # The oscillatory part is bounded by sqrt(dx^2 + dy^2) = radius.
        # So x(t) ~ vx0*t + bounded_term.
        # If vx0 > 0, eventually x(t) > wall_x.
        
        # Let's verify f(high)
        val_high = get_x_at_time(high, x0, y0) - wall_x
        if val_high < 0:
            # It hasn't reached the wall by high time? 
            # This shouldn't happen if vx0 > 0 and high is large enough.
            # Increase high?
            # Let's just set a very large high.
            high = 10000.0
            val_high = get_x_at_time(high, x0, y0) - wall_x
            if val_high < 0:
                # Still not reached? Maybe vx0 is very small or negative?
                # If vx0 <= 0, it might never hit.
                continue

        # Binary search
        # We need to be careful about oscillations. We want the FIRST time it hits.
        # Since x(t) is roughly increasing (vx0 > 0), the first time it crosses wall_x from below is the answer.
        # However, if the oscillation is large, it might cross, go back, cross again.
        # We want the smallest t.
        # Binary search works if the function is monotonic or if we are looking for the first crossing in a range where it's monotonic.
        # Given the constraints and typical physics problems, the first crossing is usually the one we want.
        # But strictly, f(t) is not monotonic.
        # However, the "first" hit implies the smallest t > 0.
        # We can search in small intervals or use a method that finds the first root.
        # Given the smoothness and the fact that vx0 > 0, the function starts negative and goes positive.
        # The first time it becomes >= 0 is the hit.
        # But it might dip below again.
        # We can use a root finding method that finds the first root.
        # Or simply binary search on the interval [0, T] where we know it crosses.
        # Since we established f(0) < 0 and f(high) > 0, there is at least one root.
        # Is it guaranteed to be the first one?
        # If the function oscillates, there could be multiple roots.
        # But the "first" hit is the smallest t.
        # Binary search finds a root, but not necessarily the first if there are multiple.
        # However, if the function is "mostly" increasing, the first root is near where it crosses zero initially.
        # Let's try to refine: we can search in steps or use a more robust method.
        # Given the problem constraints (n <= 20, omega <= 10), the period of rotation is 2*pi/omega >= 0.6s.
        # The time to hit is likely not huge.
        # Let's try to find the root using a method that scans or uses Newton with a good initial guess.
        # Or, since we want the global minimum t, we can check intervals.
        # But simpler: The function f(t) = vx0*t + A*cos(omega*t) + B*sin(omega*t) - C.
        # Derivative f'(t) = vx0 - omega*A*sin(omega*t) + omega*B*cos(omega*t).
        # If vx0 is large enough, f is monotonic.
        # If not, it oscillates.
        # However, the problem asks for the "first" corner to hit.
        # We can iterate t from 0 upwards with a small step to find the first crossing, then refine?
        # Step size? If we step too large, we miss.
        # Better: Use a root finder that finds the first root.
        # We can use the bisection method on intervals [t_k, t_{k+1}] where sign changes.
        # But we don't know the intervals.
        # Alternative: Since we want the minimum t, and we know f(0) < 0 and f(inf) > 0,
        # and the function is continuous, the first root is the one we want.
        # We can use a hybrid approach:
        # 1. Check if f(t) becomes positive. If not, skip.
        # 2. If it does, find the root.
        # To find the first root, we can use a method that doesn't assume monotonicity but finds the smallest root.
        # One way: Use Newton's method starting from t=0? No, might converge to a later root.
        # Another way: Scan with a small step to find the first sign change, then bisect.
        # Step size: The function changes rapidly if omega is large.
        # Max derivative magnitude: |vx0| + omega * sqrt(A^2+B^2).
        # A, B are roughly 20. omega <= 10. So derivative can be ~ 10*40 = 400.
        # To resolve a root, step size should be small. Say 0.001?
        # 1000 steps per second. If T=100, 100,000 steps. For 20 vertices, 2 million ops. Feasible in Python.
        # Let's try scanning with step 0.001 until we find a sign change or exceed a reasonable time.
        # But what is a reasonable time? If vx0 is small, it could be long.
        # However, if vx0 is very small, the cookie might not hit the wall if it falls down?
        # No, wall is infinite height. It will hit eventually if vx0 > 0.
        # But if vx0 is tiny, time could be large.
        # Let's set a max time limit, say 10000 seconds.
        
        # Optimization: Instead of uniform step, we can use a smarter search.
        # But given the constraints, a careful scan might work.
        # Let's try to find the first root using a combination of scanning and bisection.
        # We'll scan with a step that ensures we don't miss a root.
        # The maximum frequency of oscillation is omega/(2pi) ~ 1.6 Hz.
        # So the function doesn't change direction too fast.
        # A step of 0.01 should be safe to detect sign changes.
        # Then bisect to refine.
        
        # Let's implement a function to find the first root for a vertex.
        
        def find_first_root(x0, y0):
            # Scan
            t = 0.0
            prev_val = get_x_at_time(t, x0, y0) - wall_x
            if prev_val >= 0:
                return 0.0 # Already at or past wall? But we assume x0 < wall_x.
            
            # Scan with step
            step = 0.01
            t_max = 10000.0
            found = False
            root_t = -1.0
            
            while t < t_max:
                t_next = t + step
                if t_next > t_max:
                    break
                curr_val = get_x_at_time(t_next, x0, y0) - wall_x
                
                if curr_val >= 0:
                    # Sign change or reached
                    # Bisect between t and t_next
                    low = t
                    high = t_next
                    for _ in range(50):
                        mid = (low + high) / 2
                        mid_val = get_x_at_time(mid, x0, y0) - wall_x
                        if mid_val >= 0:
                            high = mid
                        else:
                            low = mid
                    return high
                t = t_next
                prev_val = curr_val
            
            return -1.0

        root_t = find_first_root(x0, y0)
        if root_t > 0 and root_t < best_time:
            best_time = root_t
            best_vertex_idx = i + 1

    print(f"{best_vertex_idx} {best_time:.6f}")

if __name__ == "__main__":
    solve()