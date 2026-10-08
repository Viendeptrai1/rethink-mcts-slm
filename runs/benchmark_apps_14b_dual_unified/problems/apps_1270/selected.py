import sys

def is_prime(num):
    if num <= 1:
        return False
    if num <= 3:
        return True
    if num % 2 == 0 or num % 3 == 0:
        return False
    i = 5
    while i * i <= num:
        if num % i == 0 or num % (i + 2) == 0:
            return False
        i += 6
    return True

def find_primes(n):
    if n == 2:
        return [2]
    if n == 3:
        return [3]
    if n % 2 == 0:
        return [2] + find_primes(n - 2)
    else:
        if is_prime(n - 2):
            return [2, n - 2]
        else:
            return [3] + find_primes(n - 3)

def main():
    import sys
    n = int(sys.stdin.read().strip())
    primes = find_primes(n)
    print(len(primes))
    print(" ".join(map(str, primes)))

if __name__ == "__main__":
    main()