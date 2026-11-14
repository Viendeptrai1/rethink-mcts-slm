import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    K = int(data[1])
    Q = int(data[2])
    
    A = []
    idx = 3
    for _ in range(Q):
        A.append(int(data[idx]))
        idx += 1
    
    count = [0] * (N + 1)
    for player in A:
        count[player] += 1
    
    results = []
    for i in range(1, N + 1):
        survived = K - (Q - count[i]) > 0
        if survived:
            results.append("Yes")
        else:
            results.append("No")
    
    print("\n".join(results))

if __name__ == "__main__":
    solve()