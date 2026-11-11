import math

def find_n_from_factorial(factorial_value):
    n = 1
    while True:
        if math.factorial(n) == int(factorial_value):
            return n
        elif math.factorial(n) > int(factorial_value):
            return n - 1
        n += 1

if __name__ == "__main__":
    import sys
    factorial_value = sys.stdin.read().strip()
    print(find_n_from_factorial(factorial_value))