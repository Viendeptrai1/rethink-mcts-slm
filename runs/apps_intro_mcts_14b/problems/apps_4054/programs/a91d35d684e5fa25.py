import sys

def count_even_numbers(numbers):
    return sum(1 for num in numbers if num % 2 == 0)

if __name__ == "__main__":
    input_line = sys.stdin.read().strip()
    numbers = list(map(int, input_line.split()))
    result = count_even_numbers(numbers)
    print(result)