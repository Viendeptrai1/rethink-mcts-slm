import sys

def count_trailing_zeros(n):
    count = 0
    while n % 10 == 0:
        count += 1
        n //= 10
    return count

def main():
    n = int(sys.stdin.read().strip())
    result = count_trailing_zeros(n)
    print(result)

if __name__ == "__main__":
    main()