import sys
import math

def find_factorial_n(factorial_value):
    low, high = 1, 10**6
    while low < high:
        mid = (low + high) // 2
        if math.factorial(mid) < factorial_value:
            low = mid + 1
        else:
            high = mid
    return low

if __name__ == "__main__":
    input_data = sys.stdin.read().strip()
    factorial_value = int(input_data)
    result = find_factorial_n(factorial_value)
    print(result)