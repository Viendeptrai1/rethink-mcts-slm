import sys
from math import isclose

def calculate_area(vertices):
    n = len(vertices)
    area = 0
    for i in range(n):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % n]
        area += x1 * y2 - x2 * y1
    return abs(area) / 2

def find_bulkhead_placements(C, vertices):
    total_area = calculate_area(vertices)
    M = int(total_area // C) + 1
    
    placements = []
    for i in range(1, M):
        ratio = i / M
        x_min, y_min = min(vertices, key=lambda p: p[0])[0], min(vertices, key=lambda p: p[1])[1]
        x_max, y_max = max(vertices, key=lambda p: p[0])[0], max(vertices, key=lambda p: p[1])[1]
        
        x_placement = x_min + ratio * (x_max - x_min)
        placements.append(x_placement)
    
    return M, placements

def main():
    input = sys.stdin.read
    data = input().split()
    
    C = int(data[0])
    N = int(data[1])
    vertices = [(int(data[i * 2 + 2]), int(data[i * 2 + 3])) for i in range(N)]
    
    M, placements = find_bulkhead_placements(C, vertices)
    
    print(M)
    for placement in placements:
        print(f"{placement:.6f}")

if __name__ == "__main__":
    main()