import sys

def find_largest_number():
    import sys
    n = int(sys.stdin.readline().strip())
    numbers = list(map(int, sys.stdin.readline().strip().split()))
    largest_number = max(numbers)
    return largest_number

if __name__ == "__main__":
    result = find_largest_number()
    print(result)