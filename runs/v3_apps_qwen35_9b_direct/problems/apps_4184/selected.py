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
    
    total_sum = sum(W)
    min_diff = float('inf')
    
    # T ranges from 1 to N-1
    # Group 1: indices 0 to T-1 (first T elements)
    # Group 2: indices T to N-1 (remaining elements)
    current_s1 = 0
    for T in range(1, N):
        current_s1 += W[T-1]
        current_s2 = total_sum - current_s1
        diff = abs(current_s1 - current_s2)
        if diff < min_diff:
            min_diff = diff
            
    print(min_diff)

if __name__ == "__main__":
    solve()