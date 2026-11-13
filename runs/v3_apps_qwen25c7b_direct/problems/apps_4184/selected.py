import sys

def min_difference(N, W):
    total_sum = sum(W)
    min_diff = float('inf')
    
    for T in range(1, N):
        S1 = sum(W[:T])
        S2 = total_sum - S1
        diff = abs(S1 - S2)
        if diff < min_diff:
            min_diff = diff
    
    return min_diff

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    N = int(data[0])
    W = list(map(int, data[1:]))
    result = min_difference(N, W)
    print(result)