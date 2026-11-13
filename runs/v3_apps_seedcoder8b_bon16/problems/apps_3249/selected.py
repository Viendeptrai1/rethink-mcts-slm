import sys
import math
from itertools import combinations

def area(x1, y1, x2, y2, x3, y3):
    return abs((x1*(y2-y3) + x2*(y3-y1) + x3*(y1-y2)) / 2.0)

def find_bulkhead_placements(C, vertices):
    N = len(vertices)
    hull_areas = [area(*vertices[i], *vertices[(i+1) % N], *vertices[(i+2) % N]) for i in range(N)]
    total_hull_area = sum(hull_areas)
    perimeter_length = sum(math.sqrt((vertices[i][0] - vertices[(i-1) % N][0])**2 + (vertices[i][1] - vertices[(i-1) % N][1])**2) for i in range(N))
    
    # Calculate the possible number of bulkhead sections
    M = int(total_hull_area // C) + 1

    bulkhead_positions = []
    
    for k in range(1, M):
        target_area = k * C
        for (i, (x1, y1)), (j, (x2, y2)) in combinations(enumerate(vertices), 2):
            edge_length = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            
            if edge_length == 0:
                continue

            # Calculate the area between these points assuming they form a rectangle
            edge_area = min(area(x1, y1, x2, y2, *vertices[(j+1) % N]), area(x1, y1, x2, y2, *vertices[(i+1) % N]))
            num_sections = edge_area / C

            if num_sections.is_integer():
                pos = x1 + (x2 - x1) * (target_area / edge_area)
                bulkhead_positions.append(pos)

    bulkhead_positions = sorted(set(bulkhead_positions))
    return [M] + bulkhead_positions

def main():
    input = sys.stdin.read
    data = input().strip().split()
    
    C = int(data[0])
    N = int(data[1])
    vertices = [(int(data[i*2+2]), int(data[i*2+3])) for i in range(N)]
    
    result = find_bulkhead_placements(C, vertices)
    
    for num in result:
        print(f"{num:.6f}")

if __name__ == "__main__":
    main()