def bachgold(n):
    primes = []
    while n > 3:
        primes.append(2)
        n -= 2
    if n == 3:
        primes.append(3)
    elif n == 2:
        primes.append(2)
    return len(primes), primes

# Example usage:
n = int(input())
k, primes = bachgold(n)
print(k)
print(*primes)