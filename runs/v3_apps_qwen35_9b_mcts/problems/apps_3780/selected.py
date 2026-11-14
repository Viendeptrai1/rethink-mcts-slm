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
    
    vx1 = int(next(iterator))
    vy1 = int(next(iterator))
    
    vx2 = int(next(iterator))
    vy2 = int(next(iterator))
    
    # Target relative to start
    dx = x2 - x1
    dy = y2 - y1
    
    # Wind vectors
    # Phase 1: duration t, vector (vx1, vy1)
    # Phase 2: duration (T - t), vector (vx2, vy2)
    
    # The problem asks for minimum time T.
    # The set of reachable points at time T is a disk centered at:
    # C = (vx1 * t + vx2 * (T - t), vy1 * t + vy2 * (T - t))
    # with radius R = v_max * T.
    # We need the target (dx, dy) to be on the boundary of this disk for the minimum time.
    # So, distance((0,0), C) = R.
    # sqrt( (dx - Cx)^2 + (dy - Cy)^2 ) = v_max * T
    
    # Let's define the wind drift components as functions of T.
    # Cx(T) = vx1 * t + vx2 * (T - t) = vx2 * T + t * (vx1 - vx2)
    # Cy(T) = vy1 * t + vy2 * (T - t) = vy2 * T + t * (vy1 - vy2)
    
    # Let A = vx2, B = vy2
    # Let C_const = t * (vx1 - vx2), D_const = t * (vy1 - vy2)
    # Cx = A * T + C_const
    # Cy = B * T + D_const
    
    # Equation: (dx - (A*T + C_const))^2 + (dy - (B*T + D_const))^2 = (v_max * T)^2
    
    # Expand:
    # (dx - C_const - A*T)^2 + (dy - D_const - B*T)^2 = v_max^2 * T^2
    # Let Kx = dx - C_const, Ky = dy - D_const
    # (Kx - A*T)^2 + (Ky - B*T)^2 = v_max^2 * T^2
    # Kx^2 - 2*Kx*A*T + A^2*T^2 + Ky^2 - 2*Ky*B*T + B^2*T^2 = v_max^2 * T^2
    # (A^2 + B^2 - v_max^2) * T^2 - 2*(Kx*A + Ky*B) * T + (Kx^2 + Ky^2) = 0
    
    A = vx2
    B = vy2
    C_const = t * (vx1 - vx2)
    D_const = t * (vy1 - vy2)
    
    Kx = dx - C_const
    Ky = dy - D_const
    
    # Coefficients for quadratic equation: a*T^2 + b*T + c = 0
    a = (A*A + B*B) - (v_max * v_max)
    b = -2 * (Kx * A + Ky * B)
    c = Kx * Kx + Ky * Ky
    
    # Solve quadratic equation
    discriminant = b*b - 4*a*c
    
    # Since a solution is guaranteed to exist and be positive (physically reachable),
    # and given the constraints (wind speed < v_max), 'a' will be negative.
    # Wait, A^2 + B^2 is wind_speed^2. v_max^2 is ship_speed^2.
    # Wind speed < v_max, so A^2 + B^2 < v_max^2.
    # Therefore, a = (wind_speed^2) - v_max^2 < 0.
    # Since a < 0, the parabola opens downwards.
    # c = distance^2 > 0.
    # The product of roots c/a is negative, so one root is positive and one is negative.
    # We want the positive root.
    
    if discriminant < 0:
        # This should not happen based on problem statement guarantees
        return

    sqrt_disc = math.sqrt(discriminant)
    
    # Roots: (-b +/- sqrt_disc) / (2*a)
    # Since a is negative, to get the positive root, we need to be careful with signs.
    # Let's just compute both and pick the positive one.
    
    root1 = (-b + sqrt_disc) / (2 * a)
    root2 = (-b - sqrt_disc) / (2 * a)
    
    ans = max(root1, root2)
    
    # Just a sanity check, though mathematically one must be positive
    if ans < 0:
        # Fallback if logic flipped (unlikely given constraints)
        ans = min(root1, root2)
        
    print(f"{ans:.20f}")

if __name__ == '__main__':
    solve()