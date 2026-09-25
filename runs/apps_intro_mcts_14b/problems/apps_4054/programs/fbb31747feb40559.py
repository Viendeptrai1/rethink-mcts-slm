import sys

def find_smallest_odd_number(numbers):
    odd_numbers = [num for num in numbers if num % 2 != 0]
    if odd_numbers:
        return min(odd_numbers)
    else:
        return -1

if __name__ == "__main__":
    input_line = sys.stdin.read().strip()
    numbers = list(map(int, input_line.split()))
    result = find_smallest_odd_number(numbers)
    print(result)