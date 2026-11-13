import math
import sys

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
        
        initial_vertices = []
        for _ in range(n):
            x = float(next(iterator))
            y = float(next(iterator))
            initial_vertices.append((x, y))
    except StopIteration:
        return

    # Convert initial angle to radians (counter-clockwise from +x)
    theta_rad = math.radians(theta_deg)
    
    # Initial velocity components
    vx = v0 * math.cos(theta_rad)
    vy = v0 * math.sin(theta_rad)
    
    # Gravity
    g = 9.81
    
    # Wall is at x = w. Since v0 >= 1 and theta in [0, 80], vx > 0.
    # Time to reach wall for a particle starting at (x0, y0) with velocity (vx, vy):
    # x(t) = x0 + vx * t = w  => t = (w - x0) / vx
    
    # Angular velocity is clockwise. 
    # Rotation matrix for clockwise rotation by angle alpha:
    # [ cos(alpha)  sin(alpha) ]
    # [-sin(alpha)  cos(alpha) ]
    # But we can also think of it as rotating the point counter-clockwise by -alpha.
    # Let's define the rotation function.
    # If a point P is rotated clockwise by alpha around origin (0,0):
    # x' = x*cos(alpha) + y*sin(alpha)
    # y' = -x*sin(alpha) + y*cos(alpha)
    
    def rotate_point(x, y, alpha):
        # alpha is clockwise rotation angle
        cos_a = math.cos(alpha)
        sin_a = math.sin(alpha)
        return (x * cos_a + y * sin_a, -x * sin_a + y * cos_a)

    best_time = float('inf')
    best_index = -1

    # Precompute time to reach wall for each vertex based on initial position
    # This avoids solving quadratic equations for time if vx is constant (which it is)
    # Wait, the x-motion is NOT affected by rotation or gravity.
    # x(t) = x0 + vx * t.
    # So time to hit wall is solely determined by initial x position and vx.
    # t_hit = (w - x0) / vx
    # This is true because rotation happens around the center of mass, 
    # and the problem states "their center of mass follows an ideal parabola".
    # The vertices rotate around the center of mass.
    # So the x-coordinate of a vertex at time t is:
    # x_v(t) = x_cm(t) + dx_rot(t)
    # where x_cm(t) = x_cm0 + vx * t
    # and dx_rot(t) is the x-offset of the vertex relative to CM due to rotation.
    
    # First, calculate the center of mass (centroid) of the polygon.
    # For a polygon with vertices (x1,y1)...(xn,yn) in counter-clockwise order:
    # Area = 0.5 * sum(x_i*y_{i+1} - x_{i+1}*y_i)
    # Cx = (1/(6*Area)) * sum( (x_i + x_{i+1}) * (x_i*y_{i+1} - x_{i+1}*y_i) )
    # Cy = (1/(6*Area)) * sum( (y_i + y_{i+1}) * (x_i*y_{i+1} - x_{i+1}*y_i) )
    
    cx0, cy0 = 0.0, 0.0
    sum_area_term_x = 0.0
    sum_area_term_y = 0.0
    
    for i in range(n):
        x1, y1 = initial_vertices[i]
        x2, y2 = initial_vertices[(i+1)%n]
        cross = x1 * y2 - x2 * y1
        sum_area_term_x += (x1 + x2) * cross
        sum_area_term_y += (y1 + y2) * cross
    
    double_area = 0.5 * sum(cross for (x1, y1), (x2, y2) in zip(initial_vertices, initial_vertices[1:] + [initial_vertices[0]]))
    # Actually let's recompute double_area properly to be safe
    double_area_val = 0.0
    for i in range(n):
        x1, y1 = initial_vertices[i]
        x2, y2 = initial_vertices[(i+1)%n]
        double_area_val += x1 * y2 - x2 * y1
    
    area_val = 0.5 * double_area_val
    if area_val == 0:
        # Should not happen based on problem statement
        return

    cx0 = sum_area_term_x / (6.0 * area_val)
    cy0 = sum_area_term_y / (6.0 * area_val)

    # Time to reach the wall is constant for all points because vx is constant
    # t_wall = (w - cx0) / vx ? NO.
    # The wall is hit when ANY part of the cookie hits x = w.
    # We need to find for each vertex i, the time t such that x_v_i(t) = w.
    # x_v_i(t) = x_cm(t) + (x_i_rotated_about_cm_at_time_t)
    # x_cm(t) = cx0 + vx * t
    # The rotation angle at time t is alpha(t) = omega * t (clockwise)
    # Let's define the vector from CM to vertex i at t=0:
    # dx_i0 = x_i - cx0
    # dy_i0 = y_i - cy0
    # At time t, this vector is rotated clockwise by alpha = omega * t.
    # x_offset(t) = dx_i0 * cos(alpha) + dy_i0 * sin(alpha)
    # y_offset(t) = -dx_i0 * sin(alpha) + dy_i0 * cos(alpha)
    # So x_v_i(t) = cx0 + vx * t + dx_i0 * cos(omega*t) + dy_i0 * sin(omega*t)
    # We need to solve for t: cx0 + vx * t + dx_i0 * cos(omega*t) + dy_i0 * sin(omega*t) = w
    # => vx * t + dx_i0 * cos(omega*t) + dy_i0 * sin(omega*t) = w - cx0
    
    # This is a transcendental equation. We can use numerical methods (e.g., Newton-Raphson or bisection).
    # Given constraints and typical physics problems, bisection is robust.
    # Range for t: [0, some_upper_bound].
    # Max x displacement due to rotation is roughly max_dist * 1.
    # Max time roughly (w - min_x_initial) / min_vx.
    # w <= 500, vx >= 1. t could be up to ~500.
    
    # Let's define the function f_i(t) = x_v_i(t) - w
    # We want root of f_i(t) = 0.
    
    # Since we need the FIRST vertex to hit, we can solve for each vertex independently
    # and pick the smallest positive t.
    
    # However, solving n equations might be slow if not careful, but n <= 20, so it's fine.
    
    results = []
    
    for idx in range(n):
        x_start, y_start = initial_vertices[idx]
        dx0 = x_start - cx0
        dy0 = y_start - cy0
        
        # Function: f(t) = vx*t + dx0*cos(omega*t) + dy0*sin(omega*t) - (w - cx0)
        # We want f(t) = 0.
        # Note: if omega is 0, cos(0)=1, sin(0)=0 -> linear equation.
        
        target_x = w - cx0
        
        def f(t):
            if omega == 0:
                return vx * t + dx0 - target_x
            else:
                return vx * t + dx0 * math.cos(omega * t) + dy0 * math.sin(omega * t) - target_x
        
        # Derivative for Newton method (optional, but good for speed)
        def df(t):
            if omega == 0:
                return vx
            else:
                return vx - dx0 * omega * math.sin(omega * t) + dy0 * omega * math.cos(omega * t)
        
        # Find a bracket [a, b] such that f(a) and f(b) have different signs.
        # t=0: f(0) = dx0 - target_x.
        # As t -> infinity, vx*t dominates, so f(t) -> +infinity (since vx > 0).
        # So if f(0) >= 0, the root is at t=0 or very close? 
        # Wait, if f(0) >= 0, it means at t=0, the point is already at or past the wall?
        # But the problem implies the cookie is thrown TOWARDS the wall.
        # And we assume the first vertex hits "for at least 10^-3 seconds", implying t > 0.
        # If f(0) >= 0, then t=0 is a solution (or the vertex is already past the wall).
        # However, physically, the cookie is thrown from somewhere.
        # If a vertex starts past the wall, it's already "hit". But usually inputs are valid such that t > 0.
        # Let's assume f(0) < 0 typically. If f(0) >= 0, then t=0 is the answer? 
        # The problem says "compute which ... hits the wall first". If it starts at the wall, t=0.
        
        # Let's use bisection. Lower bound 0. Upper bound?
        # Since vx >= 1 and w <= 500, max t is roughly 500 + some margin. Let's use 2000 to be safe.
        
        a = 0.0
        b = 2000.0
        
        fa = f(a)
        # Ensure fb has opposite sign or we adjust b
        # If fa >= 0, then t=0 is a root. But let's check if it's exactly 0 or slightly positive.
        # Given "first vertex to hit ... for at least 10^-3 seconds", maybe t=0 is not the case for the "first" hit unless multiple hit at 0?
        # But we just need the smallest t >= 0.
        
        if fa >= 0:
            # The point is at or beyond the wall at t=0.
            # Is this possible? "thrown against a wall". Usually starts before.
            # If it starts at or past, t=0.
            t_sol = 0.0
        else:
            # f(a) < 0. Since f(t) -> inf, there is a root in (0, b].
            # Find b such that f(b) > 0.
            # Linear growth vx*t ensures we will find it eventually.
            # Let's expand b until f(b) > 0.
            while f(b) < 0:
                b *= 2
                if b > 1e9:
                    break # Should not happen
            
            fb = f(b)
            
            # Bisection
            for _ in range(100): # 100 iterations gives sufficient precision
                mid = (a + b) / 2.0
                fm = f(mid)
                if fm >= 0:
                    b = mid
                else:
                    a = mid
            t_sol = (a + b) / 2.0
        
        # Verify t_sol is non-negative
        if t_sol < 0:
            t_sol = 0.0
            
        results.append((t_sol, idx + 1))
    
    # Find minimum time
    results.sort(key=lambda x: x[0])
    
    best_t, best_idx = results[0]
    
    # Format output
    # T_i must be given with an absolute error of less than 10^-3.
    # Print index and time.
    print(f"{best_idx} {best_t:.6f}")

if __name__ == "__main__":
    solve()