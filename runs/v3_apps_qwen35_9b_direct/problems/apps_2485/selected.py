import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return
    
    H = int(data[0])
    W = int(data[1])
    M = int(data[2])
    
    h = [0] * M
    w = [0] * M
    
    idx = 3
    for i in range(M):
        h[i] = int(data[idx])
        w[i] = int(data[idx+1])
        idx += 2
    
    # Count targets in each row and each column
    row_count = [0] * (H + 1)
    col_count = [0] * (W + 1)
    
    for i in range(M):
        row_count[h[i]] += 1
        col_count[w[i]] += 1
    
    # Find the maximum number of targets in any single row or column
    max_targets = 0
    for i in range(1, H + 1):
        if row_count[i] > max_targets:
            max_targets = row_count[i]
    
    for i in range(1, W + 1):
        if col_count[i] > max_targets:
            max_targets = col_count[i]
    
    print(max_targets)

if __name__ == '__main__':
    solve()