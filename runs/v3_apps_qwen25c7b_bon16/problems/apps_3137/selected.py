import sys
from collections import deque

def main():
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    N = int(data[index])
    M = int(data[index + 1])
    K = int(data[index + 2])
    T_X = int(data[index + 3]) - 1
    T_Y = int(data[index + 4]) - 1
    
    index += 5
    bacteria = []
    grid = []
    
    for _ in range(K):
        X_i = int(data[index]) - 1
        Y_i = int(data[index + 1]) - 1
        C_i = data[index + 2]
        
        X_values = [int(data[index + 3 + j * (M + 1)]) for j in range(N)]
        grid.append(X_values)
        
        if C_i == 'U':
            direction = (-1, 0)
        elif C_i == 'R':
            direction = (0, 1)
        elif C_i == 'D':
            direction = (1, 0)
        else:
            direction = (0, -1)
        
        bacteria.append((X_i, Y_i, direction))
    
    visited = [[False] * M for _ in range(N)]
    queue = deque([(bacteria[i][0], bacteria[i][1], i) for i in range(K)])
    time = 0
    
    while queue:
        for _ in range(len(queue)):
            x, y, i = queue.popleft()
            
            if x == T_X and y == T_Y:
                return time
            
            dx, dy = bacteria[i][2]
            bacteria[i] = ((x + dx) % N, (y + dy) % M, bacteria[i][2])
            
            new_x, new_y = bacteria[i][0], bacteria[i][1]
            visited[new_x][new_y] = True
            queue.append((new_x, new_y, i))
        
        visited = [[False] * M for _ in range(N)]
        time += 1
    
    return -1

if __name__ == "__main__":
    result = main()
    print(result)