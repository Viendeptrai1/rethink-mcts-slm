import sys
from heapq import heappop, heappush

def min_tunnel_cost(N, planets):
    # Extract coordinates
    xs = [p[0] for p in planets]
    ys = [p[1] for p in planets]
    zs = [p[2] for p in planets]
    
    # Sort coordinates
    xs.sort()
    ys.sort()
    zs.sort()
    
    # Calculate minimum differences
    dx = xs[-1] - xs[0]
    dy = ys[-1] - ys[0]
    dz = zs[-1] - zs[0]
    
    # The minimum tunnel cost is the smallest difference
    return min(dx, dy, dz)

# Read input
input = sys.stdin.read
data = input().split()

N = int(data[0])
planets = [(int(data[i*3+1]), int(data[i*3+2]), int(data[i*3+3])) for i in range(N)]

# Calculate and print the result
print(min_tunnel_cost(N, planets))