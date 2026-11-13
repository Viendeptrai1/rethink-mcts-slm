def solve():
    import sys
    input = sys.stdin.readline
    
    N, Q = map(int, input().split())
    
    def update(L, R, A, B):
        for i in range(L, R + 1):
            yield (i - L + 1) * A % B
    
    stones = [0] * (N + 1)
    prefix_sum = [0] * (N + 1)
    
    for _ in range(Q):
        query = list(map(int, input().split()))
        
        if query[0] == 1:
            L, R, A, B = query[1:]
            for i, value in zip(range(L, R + 1), update(L, R, A, B)):
                diff = value - stones[i]
                stones[i] = value
                prefix_sum[i:] = [x + diff for x in prefix_sum[i:]]
        
        else:
            L, R = query[1:]
            print(prefix_sum[R] - prefix_sum[L - 1])

solve()