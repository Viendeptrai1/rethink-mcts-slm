def solve():
    N = int(input())
    a = list(map(int, input().split()))
    
    prefix_sum = [0] * (3*N + 1)
    for i in range(3*N):
        prefix_sum[i+1] = prefix_sum[i] + a[i]
    
    max_score = float('-inf')
    for i in range(N+1):
        for j in range(i, N+i):
            score = (prefix_sum[i+j] - prefix_sum[i]) - (prefix_sum[3*N] - prefix_sum[j+N])
            max_score = max(max_score, score)
    
    print(max_score)

solve()