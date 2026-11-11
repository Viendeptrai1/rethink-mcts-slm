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

def find_primes_sum(n):
    primes = []
    for i in range(2, n + 1):
        if is_prime(i):
            primes.append(i)
    
    result = []
    for prime in reversed(primes):
        while n >= prime:
            result.append(prime)
            n -= prime
    
    return result

def main():
    import sys
    n = int(sys.stdin.read().strip())
    primes = find_primes_sum(n)
    print(len(primes))
    print(" ".join(map(str, primes)))

if __name__ == "__main__":
    main()