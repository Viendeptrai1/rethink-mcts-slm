import math

def find_n(factorial_value):
    n = 1
    while True:
        factorial_value //= n
        if factorial_value == 1:
            return n
        elif factorial_value < 1:
            return n - 1
        n += 1

# Example usage:
if __name__ == "__main__":
    import sys
    input_value = int(sys.stdin.read().strip())
    result = find_n(input_value)
    print(result)