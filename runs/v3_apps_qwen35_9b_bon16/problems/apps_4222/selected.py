import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    idx = 0
    
    N = int(data[idx]); idx += 1
    K = int(data[idx]); idx += 1
    
    has_snack = [False] * (N + 1)
    
    for _ in range(K):
        d = int(data[idx]); idx += 1
        for _ in range(d):
            snuke_id = int(data[idx]); idx += 1
            has_snack[snuke_id] = True
            
    count = 0
    for i in range(1, N + 1):
        if not has_snack[i]:
            count += 1
            
    print(count)

if __name__ == '__main__':
    solve()