from sys import stdin, stdout
import bisect

def fibonacci(limit):
    fibs = [0] * limit
    fibs[1] = 1
    for i in range(2, limit):
        fibs[i] = fibs[i - 1] + fibs[i - 2]
    return fibs

def solve():
    n, a, d = map(int, stdin.readline().strip().split())
    max_fib_index = 10**6
    fibs = fibonacci(max_fib_index)
    fib_strs = ['' for _ in range(max_fib_index)]
    
    for i in range(max_fib_index):
        fib_strs[i] = str(fibs[i])
    
    def check(b, e):
        for i in range(n):
            num = fibs[b + i * e]
            target = str(a + i * d)
            if target not in fib_strs[num].zfill(18):
                return False
        return True
    
    low, high = 1, 2**64
    while low < high:
        mid = (low + high) // 2
        if check(mid, mid):
            high = mid
        else:
            low = mid + 1
    
    if low == 2**64:
        stdout.write("-1\n")
    else:
        stdout.write(f"{low} {low}\n")

if __name__ == "__main__":
    solve()