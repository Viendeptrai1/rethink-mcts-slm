def find_arithmetic_sequence(n, a, d):
    from itertools import count

    def fibonacci():
        f0, f1 = 0, 1
        while True:
            yield f0
            f0, f1 = f1, f0 + f1

    def last_18_digits(num):
        return str(num)[-18:]

    fib_gen = fibonacci()
    for b in range(1, 2**64):
        for e in range(1, 2**64):
            valid = True
            for i in range(n):
                term_a = a + i * d
                term_b = b + i * e
                fib_term = next(fib_gen)
                while fib_term < 10**(18 + len(str(term_b))):
                    if str(term_a) in last_18_digits(fib_term):
                        break
                    fib_term = next(fib_gen)
                else:
                    valid = False
                    break
            if valid:
                return b, e
    return -1

# Read input
import sys
input = sys.stdin.read
data = input().strip().split()
n = int(data[0])
a = int(data[1])
d = int(data[2])

# Find and print the result
result = find_arithmetic_sequence(n, a, d)
if result == -1:
    print(result)
else:
    print(f"{result[0]} {result[1]}")