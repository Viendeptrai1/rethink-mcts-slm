import sys

def find_fibonacci_sequence(n, a, d):
    def fib_to_str(num):
        return str(num).zfill(18)
    
    def contains_substring(main_str, sub_str):
        return sub_str in main_str
    
    for b in range(1, 2**64):
        found = True
        for i in range(n):
            fib_num = fib(b + i * d)
            if not contains_substring(fib_to_str(fib_num), fib_to_str(a + i * d)):
                found = False
                break
        if found:
            return b, d
    return -1

def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b

# Input reading
input = sys.stdin.read
data = input().split()
n = int(data[0])
a = int(data[1])
d = int(data[2])

# Output result
result = find_fibonacci_sequence(n, a, d)
print(result)