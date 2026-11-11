import sys

def min_absolute_difference(N, weights):
    total_sum = sum(weights)
    min_diff = float('inf')
    
    for T in range(1, N):
        S1 = sum(weights[:T])
        S2 = total_sum - S1
        diff = abs(S1 - S2)
        if diff < min_diff:
            min_diff = diff
    
    return min_diff

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    N = int(data[0])
    weights = list(map(int, data[1:]))
    result = min_absolute_difference(N, weights)
    print(result)