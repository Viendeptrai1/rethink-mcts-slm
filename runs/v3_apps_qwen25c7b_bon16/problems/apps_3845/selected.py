import sys
from typing import List

def generate_grid(A: int, B: int) -> None:
    if A == 1 and B == 1:
        print(1, 1)
        print('#')
        return
    
    h = max(A, B)
    w = h
    
    grid = [['.' for _ in range(w)] for _ in range(h)]
    
    def fill_components(x: int, y: int, color: str) -> None:
        if x < 0 or x >= h or y < 0 or y >= w or grid[x][y] != '.':
            return
        grid[x][y] = color
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            fill_components(x + dx, y + dy, color)
    
    def place_components() -> None:
        count = 0
        for i in range(h):
            for j in range(w):
                if grid[i][j] == '.' and count < A:
                    fill_components(i, j, '#')
                    count += 1
        
        count = 0
        for i in range(h):
            for j in range(w):
                if grid[i][j] == '.' and count < B:
                    fill_components(i, j, '.')
                    count += 1
    
    place_components()
    
    print(h, w)
    for row in grid:
        print(''.join(row))

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    A = int(data[0])
    B = int(data[1])
    generate_grid(A, B)