def fibonacci_sequence(limit):
    fibs = [0, 1]
    while True:
        next_fib = fibs[-1] + fibs[-2]
        if next_fib > limit:
            break
        fibs.append(next_fib)
    return fibs

def find_arithmetic_sequence(n, a, d):
    max_fib = 10**18
    fibs = fibonacci_sequence(max_fib)
    
    for b in range(1, len(fibs)):
        for e in range(1, len(fibs)):
            valid = True
            for i in range(n):
                fib = fibs[b + i * e]
                if str(a + i * d) not in str(fib)[-18:]:
                    valid = False
                    break
            if valid:
                return b, e
    return -1, -1

import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
a = int(data[1])
d = int(data[2])

b, e = find_arithmetic_sequence(n, a, d)
print(b, e)