import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    d = [int(data[i+1]) for i in range(N)]
    
    d.sort()
    
    # We need exactly N/2 problems in ARC and N/2 in ABC.
    # Let target = N // 2.
    # Problems with difficulty >= K go to ARC.
    # Problems with difficulty < K go to ABC.
    # To have exactly target problems in ARC, we need the target-th smallest difficulty (0-indexed) to be the threshold.
    # Specifically, if we sort difficulties:
    # d[0], d[1], ..., d[N-1]
    # We want indices 0 to target-1 to be ABC (< K) and indices target to N-1 to be ARC (>= K).
    # This requires:
    # K > d[target-1]  (so that d[target-1] is in ABC)
    # K <= d[target]   (so that d[target] is in ARC)
    
    target = N // 2
    lower_bound = d[target - 1]
    upper_bound = d[target]
    
    # K must be an integer such that lower_bound < K <= upper_bound.
    # The number of such integers is upper_bound - lower_bound.
    # Example: if lower=4, upper=6, then K can be 5, 6 -> count = 2 = 6-4.
    # If lower=6, upper=6, then no K satisfies 6 < K <= 6 -> count = 0.
    
    ans = upper_bound - lower_bound
    print(ans)

if __name__ == '__main__':
    solve()