import sys

def simulate_bacteria(N, M, K, trap_row, trap_col, bacteria):
    directions = {'U': (-1, 0), 'R': (0, 1), 'D': (1, 0), 'L': (0, -1)}
    visited = set()
    
    def move(x, y, d, X):
        dx, dy = directions[d]
        for _ in range(X):
            nx, ny = x + dx, y + dy
            if 1 <= nx <= N and 1 <= ny <= M:
                d = directions[list(directions.keys())[list(directions.values()).index((dx, dy)) + 1]]
                dx, dy = directions[d]
            else:
                d = list(directions.keys())[list(directions.values()).index((dx, dy)) + 2]
                dx, dy = directions[d]
            x, y = nx, ny
        return x, y
    
    for i in range(K):
        x, y, d, X = bacteria[i]
        while True:
            x, y = move(x, y, d, X)
            if (x, y) == (trap_row, trap_col):
                return i + 1
            if (x, y) in visited:
                break
            visited.add((x, y))
    return -1

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    M = int(data[1])
    K = int(data[2])
    trap_row = int(data[3])
    trap_col = int(data[4])
    
    bacteria = []
    index = 5
    for i in range(K):
        x = int(data[index])
        y = int(data[index + 1])
        d = data[index + 2]
        matrix = [data[index + 3 + j * M:index + 3 + (j + 1) * M] for j in range(N)]
        bacteria.append((x, y, d, int(matrix[x-1][y-1])))
        index += 3 + N * M
    
    result = simulate_bacteria(N, M, K, trap_row, trap_col, bacteria)
    print(result)