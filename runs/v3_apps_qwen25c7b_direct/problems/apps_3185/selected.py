import math

def find_n_from_factorial(factorial_value):
    n = 0
    while math.factorial(n) < factorial_value:
        n += 1
    return n if math.factorial(n) == factorial_value else None

# Example usage:
if __name__ == "__main__":
    import sys
    input_value = int(sys.stdin.read().strip())
    result = find_n_from_factorial(input_value)
    print(result)