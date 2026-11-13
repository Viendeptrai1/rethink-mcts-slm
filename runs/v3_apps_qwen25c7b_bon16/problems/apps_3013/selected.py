import sys
import math

def find_release_point(b, tx, ty):
    def spiral_to_cartesian(r, phi):
        return r * math.cos(phi), r * math.sin(phi)
    
    def cartesian_to_spiral(x, y):
        r = math.sqrt(x**2 + y**2)
        phi = math.atan2(y, x)
        return r, phi
    
    def distance(p1, p2):
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
    
    r_t, phi_t = cartesian_to_spiral(tx, ty)
    r_t /= b
    
    def f(phi):
        r = b * phi
        x, y = spiral_to_cartesian(r, phi)
        return distance((x, y), (tx, ty))
    
    def df(phi):
        r = b * phi
        x, y = spiral_to_cartesian(r, phi)
        dx_dphi = -y / r * b
        dy_dphi = x / r * b
        return math.sqrt(dx_dphi**2 + dy_dphi**2)
    
    phi = phi_t
    while True:
        df_phi = df(phi)
        if abs(df_phi) < 1e-5:
            break
        delta_phi = -f(phi) / df_phi
        phi += delta_phi
    
    r_rel, _ = spiral_to_cartesian(b * phi, phi)
    x_rel, y_rel = spiral_to_cartesian(r_rel, phi)
    
    return x_rel, y_rel

# Read input
input_data = sys.stdin.read().strip()
b, tx, ty = map(float, input_data.split())

# Calculate and print result
result = find_release_point(b, tx, ty)
print(f"{result[0]:.10f} {result[1]:.10f}")