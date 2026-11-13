import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    iterator = iter(data)
    
    N = int(next(iterator))
    K = int(next(iterator))
    
    has_snack = [False] * (N + 1)
    
    for _ in range(K):
        d = int(next(iterator))
        for _ in range(d):
            a = int(next(iterator))
            has_snack[a] = True
    
    count = 0
    for i in range(1, N + 1):
        if not has_snack[i]:
            count += 1
    
    print(count)

if __name__ == "__main__":
    solve()