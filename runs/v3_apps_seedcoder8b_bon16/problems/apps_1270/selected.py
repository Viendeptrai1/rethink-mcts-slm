import sys

def bachgold(n):
    if n % 2 == 0:
        return n // 2, [2] * (n // 2)
    else:
        return (n - 3) // 2 + 1, [2] * ((n - 3) // 2) + [3]

def main():
    n = int(sys.stdin.readline().strip())
    k, primes = bachgold(n)
    print(k)
    print(*primes)

if __name__ == "__main__":
    main()