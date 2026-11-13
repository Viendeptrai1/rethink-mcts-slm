import sys
from math import gcd, isclose

def area_of_triangle(x1, y1, x2, y2, x3, y3):
    return abs(x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1 - y2)) / 2

def find_bulkhead_placements():
    input = sys.stdin.read
    data = input().split()
    
    C = int(data[0])
    N = int(data[1])
    
    points = []
    index = 2
    for _ in range(N):
        x = int(data[index])
        y = int(data[index + 1])
        points.append((x, y))
        index += 2
    
    # Calculate total area of the polygon
    total_area = 0
    for i in range(N):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % N]
        total_area += area_of_triangle(0, 0, x1, y1, x2, y2)
    
    # Calculate the number of bulkheads
    M = int(total_area // C)
    
    # Find the bulkhead placements
    placements = []
    current_area = 0
    target_area = total_area / M
    
    for i in range(N):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % N]
        segment_area = area_of_triangle(0, 0, x1, y1, x2, y2)
        
        while current_area + segment_area >= target_area:
            # Calculate the intersection point of the current segment
            if x1 == x2:
                x_intersect = x1
            else:
                t = (target_area - current_area) / segment_area
                x_intersect = x1 + t * (x2 - x1)
            
            placements.append(x_intersect)
            current_area += segment_area
            if current_area >= target_area:
                break
        
        current_area += segment_area
    
    # Output the results
    print(M)
    for placement in placements:
        print(f"{placement:.6f}")