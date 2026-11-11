import math
from scipy.optimize import fsolve

def archimedean_spiral(b, phi):
    r = b * phi
    return r * math.cos(phi), r * math.sin(phi)

def target_distance(b, phi, tx, ty):
    sx, sy = archimedean_spiral(b, phi)
    return math.sqrt((sx - tx)**2 + (sy - ty)**2)

def find_release_point(b, tx, ty):
    def equation(phi):
        sx, sy = archimedean_spiral(b, phi)
        vx, vy = -b * math.sin(phi), b * math.cos(phi)
        t = (tx - sx) * vx + (ty - sy) * vy
        if t <= 0:
            return float('inf')
        px, py = sx + vx * t, sy + vy * t
        return target_distance(b, phi, tx, ty) - math.sqrt((px - tx)**2 + (py - ty)**2)
    
    phi_initial_guess = math.atan2(ty, tx)
    phi_solution = fsolve(equation, phi_initial_guess)[0]
    return archimedean_spiral(b, phi_solution)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    b = float(data[0])
    tx = float(data[1])
    ty = float(data[2])
    x, y = find_release_point(b, tx, ty)
    print(f"{x:.10f} {y:.10f}")

if __name__ == "__main__":
    main()