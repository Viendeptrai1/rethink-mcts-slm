def min_absolute_difference():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    weights = list(map(int, data[1:]))
    
    min_diff = float('inf')
    
    for T in range(1, N):
        S_1 = sum(weights[:T])
        S_2 = sum(weights[T:])
        diff = abs(S_1 - S_2)
        if diff < min_diff:
            min_diff = diff
    
    print(min_diff)

min_absolute_difference()