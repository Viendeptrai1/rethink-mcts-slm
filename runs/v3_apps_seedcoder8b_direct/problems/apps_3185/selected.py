def find_factorial_number(factorial_value):
    import math

    # Start with a reasonable guess for n
    n = 1
    # Incrementally increase n until the factorial of n is greater than or equal to the given factorial_value
    while math.factorial(n) < factorial_value:
        n += 1
    # Check if the factorial of n matches the given factorial_value
    if math.factorial(n) == factorial_value:
        return n
    else:
        return -1  # Return -1 if no such n exists, though the problem guarantees a valid input

if __name__ == "__main__":
    import sys
    input = sys.stdin.read().strip()
    factorial_value = int(input)
    result = find_factorial_number(factorial_value)
    print(result)