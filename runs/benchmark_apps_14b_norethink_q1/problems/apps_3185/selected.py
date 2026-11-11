import sys

def find_n_for_factorial(factorial_value):
    n = 1
    current_factorial = 1
    while True:
        if current_factorial == int(factorial_value):
            return n
        elif current_factorial > int(factorial_value):
            return -1
        n += 1
        current_factorial *= n

if __name__ == "__main__":
    input_value = sys.stdin.read().strip()
    result = find_n_for_factorial(input_value)
    print(result)