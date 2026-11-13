def solve():
    n = int(input())
    d = list(map(int, input().split()))
    
    total_sum = sum(d)
    prefix_sum = [0] * (n + 1)
    for i in range(n):
        prefix_sum[i + 1] = prefix_sum[i] + d[i]
    
    max_sum = 0
    for i in range(n + 1):
        for j in range(n - i + 1):
            sum1 = prefix_sum[i]
            sum3 = prefix_sum[n] - prefix_sum[n - j]
            if sum1 == sum3:
                max_sum = max(max_sum, sum1)
    
    print(max_sum)

solve()