import sys

def simulate_bacteria(N, M, K, trap_row, trap_col, bacteria):
    directions = {'U': (-1, 0), 'R': (0, 1), 'D': (1, 0), 'L': (0, -1)}
    visited = set()
    
    def move(x, y, d, X):
        dx, dy = directions[d]
        for _ in range(X):
            nx, ny = x + dx, y + dy
            if 1 <= nx <= N and 1 <= ny <= M:
                dx, dy = dy, -dx
            else:
                dx, dy = -dy, dx
            x, y = x + dx, y + dy
        return x, y
    
    for i in range(K):
        x, y, d, X = bacteria[i]
        while True:
            x, y = move(x, y, d, X)
            if (x, y) == (trap_row, trap_col):
                return i + 1
            if (x, y, d) in visited:
                break
            visited.add((x, y, d))
    
    return -1

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    N = int(data[index])
    index += 1
    M = int(data[index])
    index += 1
    K = int(data[index])
    index += 1
    
    trap_row = int(data[index])
    index += 1
    trap_col = int(data[index])
    index += 1
    
    bacteria = []
    for i in range(K):
        x = int(data[index])
        index += 1
        y = int(data[index])
        index += 1
        d = data[index]
        index += 1
        X = int(''.join(data[index:index+3]))
        index += 3
        bacteria.append((x, y, d, X))
    
    result = simulate_bacteria(N, M, K, trap_row, trap_col, bacteria)
    print(result)