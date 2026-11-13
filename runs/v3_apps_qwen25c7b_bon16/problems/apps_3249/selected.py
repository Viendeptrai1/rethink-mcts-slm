import sys
from typing import List

def read_input() -> (int, int, List[List[int]]):
    C = int(sys.stdin.readline().strip())
    N = int(sys.stdin.readline().strip())
    vertices = []
    for _ in range(N):
        x, y = map(int, sys.stdin.readline().strip().split())
        vertices.append([x, y])
    return C, N, vertices

def calculate_area(vertices: List[List[int]]) -> float:
    x1, y1 = vertices[0]
    area = 0.0
    for i in range(1, len(vertices)):
        x2, y2 = vertices[i]
        area += (x1 * y2 - y1 * x2)
    x2, y2 = vertices[-1]
    area += (x1 * y2 - y1 * x2)
    return abs(area) / 2.0

def find_bulkheads(C: int, vertices: List[List[int]]) -> List[float]:
    total_area = calculate_area(vertices)
    M = int(total_area // C) + 1
    bulkheads = []
    width = vertices[1][0] - vertices[0][0]
    step = width / (M - 1)
    for i in range(M):
        x = vertices[0][0] + i * step
        bulkheads.append(x)
    return bulkheads

def main():
    C, N, vertices = read_input()
    bulkheads = find_bulkheads(C, vertices)
    print(len(bulkheads))
    for bulkhead in bulkheads:
        print(f"{bulkhead:.6f}")

if __name__ == "__main__":
    main()