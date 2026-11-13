import sys

def find_fibonacci_sequence(n, a, d):
    MOD = 10**18
    MAX_FIB = 10**6
    fib = [0] * (MAX_FIB + 1)
    fib[1] = 1
    
    # Precompute Fibonacci numbers modulo 10^18
    for i in range(2, MAX_FIB + 1):
        fib[i] = (fib[i - 1] + fib[i - 2]) % MOD
    
    # Convert a + id to string for easy substring checking
    target = [str(a + i * d) for i in range(n)]
    
    # Check for possible b and e
    for b in range(1, 2**64):
        found = True
        for i in range(n):
            if str(fib[b + i * e])[-len(target[i]):] != target[i]:
                found = False
                break
        if found:
            return b, e
    
    return -1

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
a = int(data[1])
d = int(data[2])

# Find and print result
result = find_fibonacci_sequence(n, a, d)
print(result[0], result[1]) if result != -1 else print(-1)