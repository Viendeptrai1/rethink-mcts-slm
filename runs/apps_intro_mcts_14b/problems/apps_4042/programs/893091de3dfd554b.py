import sys

def find_factors(n):
    for i in range(1, min(11, n + 1)):
        if n % i == 0:
            j = n // i
            if 1 <= j <= 10:
                return i, j
    return None, None

def main():
    x = float(sys.stdin.read().strip())
    floored_value = int(x * 100)
    a, b = find_factors(floored_value)
    print(a, b)

if __name__ == "__main__":
    main()