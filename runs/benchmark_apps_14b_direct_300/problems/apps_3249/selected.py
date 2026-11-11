import sys
from typing import List

def calculate_area(x1, y1, x2, y2, x3, y3):
    return abs((x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1 - y2)) / 2.0)

def find_bulkheads(C: int, N: int, vertices: List[List[int]]) -> None:
    total_area = 0
    areas = []
    
    # Calculate the total area of the polygon
    for i in range(N):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % N]
        x3, y3 = vertices[(i + 2) % N]
        area = calculate_area(x1, y1, x2, y2, x3, y3)
        total_area += area
        areas.append(area)
    
    # Determine the number of bulkheads
    M = int(total_area // C)
    
    # Calculate the target area for each bulkhead section
    target_area = total_area / M
    
    # Find the positions of the bulkheads
    current_area = 0
    bulkheads = []
    for i in range(N):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % N]
        while current_area + areas[i] > target_area:
            ratio = (target_area - current_area) / areas[i]
            x = x1 + ratio * (x2 - x1)
            bulkheads.append(x)
            current_area = target_area
            target_area += total_area / M
        current_area += areas[i]
    
    # Print the results
    print(M)
    for x in sorted(bulkheads):
        print(f"{x:.6f}")

# Read input
input = sys.stdin.read
data = input().split()
C = int(data[0])
N = int(data[1])
vertices = []
index = 2
for _ in range(N):
    x = int(data[index])
    y = int(data[index + 1])
    vertices.append([x, y])
    index += 2

# Find and print the bulkheads
find_bulkheads(C, N, vertices)