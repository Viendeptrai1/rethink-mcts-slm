import sys
from typing import List, Tuple

def solve_bacteria_game(N: int, M: int, K: int, trap: Tuple[int, int], bacteria: List[Tuple[int, int, str, List[List[int]]]]) -> int:
    def turn(direction: str, turns: int) -> str:
        directions = "URDL"
        return directions[(directions.index(direction) + turns) % 4]

    def move(x: int, y: int, direction: str) -> Tuple[int, int]:
        if direction == 'U': return x-1, y
        if direction == 'R': return x, y+1
        if direction == 'D': return x+1, y
        if direction == 'L': return x, y-1

    board = [[set() for _ in range(M)] for _ in range(N)]
    for i, (x, y, d, grid) in enumerate(bacteria):
        board[x-1][y-1].add((i, d))

    time = 0
    while True:
        time += 1
        new_board = [[set() for _ in range(M)] for _ in range(N)]

        for x in range(N):
            for y in range(M):
                for i, d in board[x][y]:
                    turns = bacteria[i][3][x][y]
                    d = turn(d, turns)
                    nx, ny = move(x, y, d)

                    if nx < 0 or nx >= N or ny < 0 or ny >= M:
                        continue

                    new_board[nx][ny].add((i, d))

        board = new_board

        if all(len(cell) == 0 for row in board for cell in row):
            return -1
        if len(board[trap[0]-1][trap[1]-1]) == K:
            return time

if __name__ == "__main__":
    N, M, K = map(int, input().split())
    X, Y = map(int, input().split())
    bacteria = []
    for _ in range(K):
        x, y, d = input().split()
        grid = [list(map(int, input().strip())) for _ in range(N)]
        bacteria.append((int(x), int(y), d, grid))

    result = solve_bacteria_game(N, M, K, (X, Y), bacteria)
    print(result)