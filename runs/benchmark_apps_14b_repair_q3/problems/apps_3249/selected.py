import sys
from typing import List

def compute_area(x1, y1, x2, y2, x3, y3):
    return abs((x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1 - y2)) / 2.0)

def find_bulkheads(C: int, N: int, vertices: List[List[int]]) -> None:
    total_area = 0
    for i in range(N):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % N]
        x3, y3 = vertices[(i + 2) % N]
        total_area += compute_area(x1, y1, x2, y2, x3, y3)
    
    target_area = total_area / C
    bulkheads = []
    current_area = 0
    
    for i in range(N):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % N]
        while True:
            x3, y3 = vertices[(i + 2) % N]
            segment_area = compute_area(x1, y1, x2, y2, x3, y3)
            if current_area + segment_area > target_area:
                t = (target_area - current_area) / segment_area
                bulkhead_x = x2 + t * (x3 - x2)
                bulkheads.append(bulkhead_x)
                break
            current_area += segment_area
            x2, y2 = x3, y3
            i = (i + 1) % N
    
    M = len(bulkheads) + 1
    print(M)
    for x in sorted(bulkheads):
        print(f"{x:.6f}")

if __name__ == "__main__":
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
    
    find_bulkheads(C, N, vertices)