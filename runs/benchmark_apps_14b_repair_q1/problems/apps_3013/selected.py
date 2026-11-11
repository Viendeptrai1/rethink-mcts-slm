import math

def find_release_point(b, tx, ty):
    def spiral_point(phi):
        r = b * phi
        return r * math.cos(phi), r * math.sin(phi)
    
    def spiral_tangent(phi):
        r = b * phi
        dx_dphi = -r * math.sin(phi)
        dy_dphi = r * math.cos(phi)
        length = math.sqrt(dx_dphi**2 + dy_dphi**2)
        return dx_dphi / length, dy_dphi / length
    
    def distance(p1, p2):
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
    
    phi = 0
    step = 0.01
    while True:
        px, py = spiral_point(phi)
        dx, dy = spiral_tangent(phi)
        line_x = px + dx * 10000
        line_y = py + dy * 10000
        line_length = math.sqrt((line_x - px)**2 + (line_y - py)**2)
        
        # Check if the line intersects the spiral
        intersects = False
        for i in range(1, int(2 * math.pi / step)):
            test_phi = i * step
            test_px, test_py = spiral_point(test_phi)
            if (test_px - px) * (line_y - py) == (test_py - py) * (line_x - px):
                intersects = True
                break
        
        if not intersects:
            break
        
        phi += step
    
    return px, py

# Read input
import sys
input = sys.stdin.read
data = input().split()
b = float(data[0])
tx = float(data[1])
ty = float(data[2])

# Find the release point
rx, ry = find_release_point(b, tx, ty)

# Print the result
print(f"{rx:.10f} {ry:.10f}")