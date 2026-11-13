import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    n = int(input_data[0])
    m = int(input_data[1])
    
    MOD = 10**9 + 7
    
    def calc_fib(k):
        if k <= 2:
            return 2
        a, b = 2, 3
        for _ in range(3, k + 1):
            a, b = b, (a + b) % MOD
        return b
    
    fib_n = calc_fib(n)
    fib_m = calc_fib(m)
    
    result = (fib_n * 2 + fib_m * 2 - 4) % MOD
    print(result)

if __name__ == "__main__":
    solve()