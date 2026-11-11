def fibonacci_mod(m):
    fib = [0, 1]
    while True:
        fib.append((fib[-1] + fib[-2]) % m)
        if fib[-2] == 0 and fib[-1] == 1:
            break
    return fib[:-2]

def find_arithmetic_sequence(n, a, d):
    MOD = 10**18
    fib = fibonacci_mod(MOD)
    
    for b in range(1, MOD):
        found = True
        for i in range(n):
            if str(a + i * d) not in str(fib[(b + i * 1) % len(fib)]):
                found = False
                break
        if found:
            return b, 1
    
    return -1, -1

import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
a = int(data[1])
d = int(data[2])

b, e = find_arithmetic_sequence(n, a, d)
print(b, e)