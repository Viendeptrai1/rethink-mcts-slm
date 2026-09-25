import sys

def find_smallest_odd(numbers):
    for number in numbers:
        if number % 2 != 0:
            return number
    return -1

def main():
    import sys
    input_line = sys.stdin.read().strip()
    numbers = list(map(int, input_line.split()))
    result = find_smallest_odd(numbers)
    print(result)

if __name__ == "__main__":
    main()