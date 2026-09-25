import sys

def find_smallest_odd(numbers):
    smallest_odd = float('inf')
    for number in numbers:
        if number % 2 != 0 and number < smallest_odd:
            smallest_odd = number
    return smallest_odd if smallest_odd != float('inf') else 1

if __name__ == "__main__":
    input_line = sys.stdin.read().strip()
    numbers = list(map(int, input_line.split()))
    result = find_smallest_odd(numbers)
    print(result)