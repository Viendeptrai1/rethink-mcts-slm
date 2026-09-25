import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().strip().split()
    numbers = list(map(int, data))
    result = sum(1 for x in numbers if x % 2 == 0)
    print(result)

if __name__ == "__main__":
    main()