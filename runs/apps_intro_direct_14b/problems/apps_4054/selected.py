import sys

def main():
    input_line = sys.stdin.readline().strip()
    numbers = list(map(int, input_line.split()))
    
    result = sum(1 for num in numbers if num % 2 == 0)
    
    print(result)

if __name__ == "__main__":
    main()