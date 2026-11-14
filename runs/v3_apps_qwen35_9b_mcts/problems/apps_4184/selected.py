import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    N = int(next(iterator))
    W = []
    for _ in range(N):
        W.append(int(next(iterator)))
    
    min_diff = float('inf')
    
    for T in range(1, N):
        S1 = sum(W[:T])
        S2 = sum(W[T:])
        diff = abs(S1 - S2)
        if diff < min_diff:
            min_diff = diff
    
    print(min_diff)

if __name__ == "__main__":
    solve()