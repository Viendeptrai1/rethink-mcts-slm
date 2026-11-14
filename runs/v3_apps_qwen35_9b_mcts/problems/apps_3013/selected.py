import sys
import math

def solve():
    input_data = sys.stdin.read().strip()
    if not input_data:
        return
    b, tx, ty = map(float, input_data.split())

    # Convert target to polar coordinates
    r_target = math.hypot(tx, ty)
    phi_target = math.atan2(ty, tx)
    # Normalize phi_target to [0, 2*pi)
    while phi_target < 0:
        phi_target += 2 * math.pi
    while phi_target >= 2 * math.pi:
        phi_target -= 2 * math.pi

    # The spiral is r = b * phi.
    # The tangent vector at angle phi has direction (cos(phi) - b*sin(phi), sin(phi) + b*cos(phi)).
    # We need to find phi such that the line from (r(phi)*cos(phi), r(phi)*sin(phi)) in the tangent direction passes through (tx, ty).
    # This leads to a function f(phi) = 0.
    # After derivation, the condition simplifies to:
    # (r - r_t) * (cos(phi) - b*sin(phi)) - (theta - theta_t) * (sin(phi) + b*cos(phi)) = 0
    # where r = b*phi, theta = phi, r_t = r_target, theta_t = phi_target.
    # Note: theta here is the angle of the release point, which is phi.
    # The term (theta - theta_t) is actually (phi - phi_target).
    # However, we must be careful with the angle difference. The cross product form in 2D for collinearity of vectors A and B is A_x*B_y - A_y*B_x = 0.
    # Vector from release point P to Target T: V = T - P.
    # Tangent vector at P: U = (-y_p, x_p) rotated by 90 deg? No.
    # Parametric: x = b*phi*cos(phi), y = b*phi*sin(phi).
    # dx/dphi = b*cos(phi) - b*phi*sin(phi)
    # dy/dphi = b*sin(phi) + b*phi*cos(phi)
    # Tangent direction U = (dx/dphi, dy/dphi).
    # Collinearity: (T_x - P_x) * U_y - (T_y - P_y) * U_x = 0.
    
    def f(phi):
        r = b * phi
        px = r * math.cos(phi)
        py = r * math.sin(phi)
        
        dx_dphi = b * math.cos(phi) - r * math.sin(phi)
        dy_dphi = b * math.sin(phi) + r * math.cos(phi)
        
        vx = tx - px
        vy = ty - py
        
        return vx * dy_dphi - vy * dx_dphi

    # We need to find phi > 0 such that f(phi) = 0.
    # The problem guarantees the target is far enough, so a solution exists.
    # Since the spiral winds outwards, we can search for phi in a range.
    # Given constraints and geometry, phi will likely be in a reasonable range.
    # Let's use a robust root finding method. Since f is continuous and likely monotonic in segments,
    # we can try to bracket the root or use Newton-Raphson with a safe fallback.
    
    # Let's analyze the behavior. As phi increases, the spiral moves out.
    # The function f(phi) represents the signed distance (scaled) from the target to the tangent line.
    # We can search for a root.
    
    # Initial guess: The target is at r_target. The release point is at r = b*phi.
    # Roughly, b*phi should be somewhat close to r_target, but the tangent direction matters.
    # Let's try a range search first to find a bracket, then refine.
    
    # Search range for phi:
    # Minimum phi: r_target / b (if we were to go radially, but we are tangent).
    # Actually, the spiral goes to infinity. The target is fixed.
    # The line from origin to target has angle phi_target.
    # The release point angle phi might be near phi_target or differ by some amount.
    # Let's scan phi from a small positive value up to a large value to find a sign change.
    
    # Lower bound for phi: must be > 0. Also r = b*phi.
    # The problem says sqrt(tx^2+ty^2) > 2*pi*b, so r_target > 2*pi*b.
    # This implies phi_target > 2*pi is not necessarily true, but r_target is large.
    # The release point r = b*phi. If phi is small, r is small.
    # We need to find phi such that the tangent hits T.
    
    # Let's define a search interval.
    # phi_min = 0.01
    # phi_max: Since r_target <= 10000*sqrt(2) approx 14142, and b >= 0.01, phi could be up to 1.4e6.
    # But typically the solution is closer. Let's try to bracket.
    
    # We can use a simple bisection or Brent's method if we find a bracket.
    # Let's try to find a bracket by scanning.
    
    phi_low = 0.01
    phi_high = 100.0 # Start with a reasonable guess
    
    # Expand phi_high until we find a sign change or exceed a safe limit
    # However, f(phi) might not change sign monotonically if we cross the target angle multiple times?
    # Actually, for a given target, there might be multiple solutions (different turns).
    # The problem asks for "the" point. Usually implies the first valid one or the one that doesn't intersect.
    # "The avatar's path after it detaches must not intersect with any part of the spiral."
    # This condition usually selects a specific solution.
    # If we detach at phi, we move along the tangent. The spiral continues for phi' > phi.
    # We need the ray from P in direction U to not intersect the spiral for t > 0.
    # Since the spiral is convex-like (in terms of winding), and we are moving away, 
    # usually the first solution encountered (smallest phi) works if the target is "outside" the spiral loop.
    # Given r_target > 2*pi*b, the target is outside the first full loop.
    # So we look for the smallest phi > 0.
    
    # Let's scan to find the first sign change.
    
    prev_phi = phi_low
    prev_val = f(prev_phi)
    
    # If prev_val is 0, we are done (unlikely)
    if abs(prev_val) < 1e-9:
        phi_sol = prev_phi
    else:
        # Search upwards
        phi_high = phi_low + 1.0
        while phi_high < 1000000: # Safety limit
            curr_val = f(phi_high)
            if abs(curr_val) < 1e-9:
                phi_sol = phi_high
                break
            if prev_val * curr_val < 0:
                # Found bracket
                break
            prev_phi = phi_high
            prev_val = curr_val
            phi_high += 1.0
            
        if abs(curr_val) < 1e-9:
            phi_sol = phi_high
        else:
            # Use bisection on [prev_phi, phi_high]
            a, b_bracket = prev_phi, phi_high
            fa, fb = prev_val, curr_val
            
            for _ in range(100):
                mid = (a + b_bracket) / 2
                fm = f(mid)
                if abs(fm) < 1e-12:
                    phi_sol = mid
                    break
                if fa * fm < 0:
                    b_bracket = mid
                    fb = fm
                else:
                    a = mid
                    fa = fm
            
            phi_sol = (a + b_bracket) / 2

    # Now we have phi_sol. Calculate the point.
    r_sol = b * phi_sol
    x_sol = r_sol * math.cos(phi_sol)
    y_sol = r_sol * math.sin(phi_sol)
    
    print(f"{x_sol} {y_sol}")

if __name__ == "__main__":
    solve()