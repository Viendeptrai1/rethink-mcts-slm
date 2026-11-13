import math

def solve_holiday_cookie_contest():
    # Read input
    n, omega, v0, theta, w = map(float, input().split())
    n = int(n)
    theta = math.radians(theta)
    
    # Read cookie vertices
    vertices = [tuple(map(float, input().split())) for _ in range(n)]
    
    # Calculate initial velocity components
    vx = v0 * math.cos(theta)
    vy = v0 * math.sin(theta)
    
    # Calculate gravity
    g = 9.81
    
    # Function to calculate time to hit wall for a vertex
    def time_to_hit_wall(x, y):
        if x == w:
            return float('inf')
        
        t1 = (w - x) / vx
        t2 = (w - x) / (vx - omega * y)
        
        if 0 <= t1 < float('inf'):
            y1 = y + vy * t1 - 0.5 * g * t1**2
            if abs(y1) <= 0.001:
                return t1
        
        if 0 <= t2 < float('inf'):
            y2 = y + vy * t2 - 0.5 * g * t2**2
            if abs(y2) <= 0.001:
                return t2
        
        return float('inf')
    
    # Find the vertex that hits the wall first
    min_time = float('inf')
    min_index = -1
    
    for i, (x, y) in enumerate(vertices, 1):
        t = time_to_hit_wall(x, y)
        if t < min_time:
            min_time = t
            min_index = i
    
    # Output result
    print(f"{min_index} {min_time:.6f}")

# Call the function to solve the problem
solve_holiday_cookie_contest()