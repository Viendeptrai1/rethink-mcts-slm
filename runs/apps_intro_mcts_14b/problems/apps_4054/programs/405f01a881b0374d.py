import sys

def main():
    input_line = sys.stdin.readline().strip()
    numbers = list(map(int, input_line.split()))
    total_sum = sum(numbers)
    print(total_sum)

if __name__ == "__main__":
    main()