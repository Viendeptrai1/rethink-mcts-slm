import sys

def main():
    a = int(sys.stdin.read().strip())
    result = 0
    while a > 0:
        a //= 2
        result += 1
    print(result)

if __name__ == "__main__":
    main()