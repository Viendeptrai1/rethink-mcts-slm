import sys
from typing import List

def calculate_area(vertices: List[List[int]]) -> float:
    n = len(vertices)
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += vertices[i][0] * vertices[j][1]
        area -= vertices[j][0] * vertices[i][1]
    return abs(area) / 2.0

def find_bulkhead_positions(C: int, N: int, vertices: List[List[int]]) -> List[float]:
    def get_subarea(x: float) -> float:
        subvertices = []
        for v in vertices:
            if v[0] < x:
                subvertices.append(v)
            elif v[0] == x:
                subvertices.append([x, v[1]])
        subvertices.sort(key=lambda v: v[1])
        return calculate_area(subvertices)

    min_x = min(vertex[0] for vertex in vertices)
    max_x = max(vertex[0] for vertex in vertices)
    bulkhead_positions = []

    while min_x <= max_x:
        mid_x = (min_x + max_x) / 2.0
        subarea = get_subarea(mid_x)
        if subarea >= C:
            bulkhead_positions.append(mid_x)
            max_x = mid_x - 1e-6
        else:
            min_x = mid_x + 1e-6

    return sorted(bulkhead_positions)

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    C = int(data[index])
    index += 1
    
    N = int(data[index])
    index += 1
    
    vertices = []
    for _ in range(N):
        x = int(data[index])
        index += 1
        y = int(data[index])
        index += 1
        vertices.append([x, y])
    
    M = len(find_bulkhead_positions(C, N, vertices))
    print(M)
    for pos in find_bulkhead_positions(C, N, vertices):
        print(f"{pos:.6f}")