def solve():
    N = int(input())
    a = list(map(int, input().split()))
    
    def max_operations(num):
        ops = 0
        while num % 2 == 0:
            num //= 2
            ops += 1
        return ops
    
    total_ops = 0
    for num in a:
        total_ops += max_operations(num)
    
    print(total_ops)

solve()