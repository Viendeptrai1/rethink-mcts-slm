import sys

def find_factors(n):
    for i in range(1, 11):
        if n % i == 0 and 1 <= n // i <= 10:
            return i, n // i
    return None, None

def main():
    x = float(sys.stdin.read().strip())
    target = int(x * 100)
    a, b = find_factors(target)
    print(a, b)

if __name__ == "__main__":
    main()