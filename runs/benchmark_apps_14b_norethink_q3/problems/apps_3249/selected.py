import sys
from typing import List, Tuple

def polygon_area(vertices: List[Tuple[int, int]]) -> float:
    n = len(vertices)
    area = 0
    for i in range(n):
        j = (i + 1) % n
        area += vertices[i][0] * vertices[j][1]
        area -= vertices[j][0] * vertices[i][1]
    return abs(area) / 2.0

def find_bulkheads(C: int, vertices: List[Tuple[int, int]]) -> Tuple[int, List[float]]:
    n = len(vertices)
    total_area = polygon_area(vertices)
    num_sections = int(total_area // C)
    
    # Calculate the cumulative areas
    cumulative_areas = [0] * n
    for i in range(n):
        j = (i + 1) % n
        triangle_area = abs(vertices[i][0] * vertices[j][1] - vertices[j][0] * vertices[i][1]) / 2.0
        cumulative_areas[i] = cumulative_areas[i - 1] + triangle_area
    
    # Find the bulkhead positions
    bulkhead_positions = []
    target_area = total_area / num_sections
    current_area = 0
    for i in range(n):
        current_area += cumulative_areas[i]
        if current_area >= target_area:
            x1, y1 = vertices[i]
            x2, y2 = vertices[(i + 1) % n]
            t = (target_area - cumulative_areas[i - 1]) / (cumulative_areas[i] - cumulative_areas[i - 1])
            bulkhead_x = x1 + t * (x2 - x1)
            bulkhead_positions.append(bulkhead_x)
            current_area = 0
    
    return num_sections, bulkhead_positions

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    C = int(data[0])
    N = int(data[1])
    vertices = [(int(data[2 + 2 * i]), int(data[3 + 2 * i])) for i in range(N)]
    
    M, bulkhead_positions = find_bulkheads(C, vertices)
    
    print(M)
    for pos in bulkhead_positions:
        print(f"{pos:.6f}")

if __name__ == "__main__":
    main()