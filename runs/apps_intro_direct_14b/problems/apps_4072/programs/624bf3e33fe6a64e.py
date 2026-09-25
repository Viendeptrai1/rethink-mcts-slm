import sys

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def main():
    a = int(sys.stdin.read().strip())
    if is_prime(a):
        print(1)
    else:
        print(0)

if __name__ == "__main__":
    main()