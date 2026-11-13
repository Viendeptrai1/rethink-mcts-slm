import sys
from itertools import product

def read_input():
    input = sys.stdin.read().strip().split('\n')
    h, w = map(int, input[0].split())
    matrix = [list(input[i + 1]) for i in range(h)]
    return h, w, matrix

def print_matrix(matrix):
    for row in matrix:
        print(''.join(map(str, row)))

def find_polyomino(matrix):
    h, w = len(matrix), len(matrix[0])
    visited = [[False] * w for _ in range(h)]
    polyomino = []

    def dfs(x, y):
        if x < 0 or x >= h or y < 0 or y >= w or visited[x][y] or matrix[x][y] == '.':
            return
        visited[x][y] = True
        polyomino.append((x, y))
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            dfs(x + dx, y + dy)

    for i in range(h):
        for j in range(w):
            if matrix[i][j] == 'X' and not visited[i][j]:
                dfs(i, j)
                return polyomino
    return []

def rotate_polyomino(polyomino):
    x_coords, y_coords = zip(*polyomino)
    min_x, min_y = min(x_coords), min(y_coords)
    rotated = [(y - min_y, x - min_x) for x, y in polyomino]
    return sorted(rotated)

def reflect_polyomino(polyomino):
    x_coords, y_coords = zip(*polyomino)
    min_x, min_y = min(x_coords), min(y_coords)
    reflected = [(x - min_x, max(y_coords) - y) for x, y in polyomino]
    return sorted(reflected)

def generate_all_transformations(polyomino):
    transformations = set()
    for _ in range(4):
        polyomino = rotate_polyomino(polyomino)
        transformations.add(tuple(polyomino))
        transformations.add(tuple(reflect_polyomino(polyomino)))
    return transformations

def can_form_k_power(matrix, polyomino, k):
    h, w = len(matrix), len(matrix[0])
    poly_transforms = generate_all_transformations(polyomino)

    def can_place(x, y, poly):
        for dx, dy in poly:
            nx, ny = x + dx, y + dy
            if nx < 0 or nx >= h or ny < 0 or ny >= w or matrix[nx][ny] != '.':
                return False
        return True

    def place_poly(x, y, poly, num):
        for dx, dy in poly:
            nx, ny = x + dx, y + dy
            matrix[nx][ny] = num

    def remove_poly(x, y, poly):
        for dx, dy in poly:
            nx, ny = x + dx, y + dy
            matrix[nx][ny] = '.'

    def backtrack(remaining):
        if remaining == 0:
            return True
        for i in range(h):
            for j in range(w):
                for poly in poly_transforms:
                    if can_place(i, j, poly):
                        place_poly(i, j, poly, k - remaining + 1)
                        if backtrack(remaining - 1):
                            return True
                        remove_poly(i, j, poly)
        return False

    return backtrack(k)

def solve():
    h, w, matrix = read_input()
    polyomino = find_polyomino(matrix)
    if not polyomino:
        print("No solution")
        return

    for k in range(2, 6):
        if can_form_k_power(matrix, polyomino, k):
            print_matrix(matrix)
            return

    print("No solution")

solve()