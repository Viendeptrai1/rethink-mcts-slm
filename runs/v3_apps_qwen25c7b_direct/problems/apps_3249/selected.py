import sys
from typing import List

def calculate_bulkhead_positions(C: int, N: int, vertices: List[List[int]]) -> List[float]:
    def get_area(x1, y1, x2, y2):
        return abs((x1 * y2) - (x2 * y1))

    def get_total_area(vertices):
        total_area = 0
        n = len(vertices)
        for i in range(n):
            j = (i + 1) % n
            total_area += get_area(vertices[i][0], vertices[i][1], vertices[j][0], vertices[j][1])
        return total_area / 2

    total_area = get_total_area(vertices)
    M = total_area // C
    bulkhead_positions = []

    for i in range(1, M):
        target_area = i * C
        current_area = 0
        for j in range(N):
            k = (j + 1) % N
            current_area += get_area(vertices[j][0], vertices[j][1], vertices[k][0], vertices[k][1])
            if current_area >= target_area:
                x_mid = (vertices[j][0] + vertices[k][0]) / 2
                bulkhead_positions.append(x_mid)
                break

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

    result = calculate_bulkhead_positions(C, N, vertices)
    
    print(len(result))
    for pos in result:
        print(f"{pos:.6f}")