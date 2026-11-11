def fibonacci(n):
    fib = [0] * (n + 1)
    fib[0], fib[1] = 0, 1
    for i in range(2, n + 1):
        fib[i] = fib[i - 1] + fib[i - 2]
    return fib

def find_arithmetic_sequence(n, a, d):
    max_fib_index = 10**6
    fib = fibonacci(max_fib_index)
    
    for b in range(1, 2**64):
        found = True
        for i in range(n):
            fib_value = fib[b + i * d]
            fib_str = str(fib_value)
            if len(fib_str) >= 18:
                fib_str = fib_str[-18:]
            if str(a + i * d) not in fib_str:
                found = False
                break
        if found:
            return b, d
    
    return -1, -1

import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
a = int(data[1])
d = int(data[2])

b, e = find_arithmetic_sequence(n, a, d)
print(b, e)