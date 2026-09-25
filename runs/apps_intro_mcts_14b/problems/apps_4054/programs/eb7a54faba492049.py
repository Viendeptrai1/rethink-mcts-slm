import sys

def find_smallest_odd(numbers):
    min_odd = float('inf')
    for num in numbers:
        if num % 2 != 0 and num < min_odd:
            min_odd = num
    return min_odd if min_odd != float('inf') else -1

if __name__ == "__main__":
    input_line = sys.stdin.read().strip()
    numbers = list(map(int, input_line.split()))
    result = find_smallest_odd(numbers)
    print(result)