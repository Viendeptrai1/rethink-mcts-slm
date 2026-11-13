def bachgold_problem(n):
    def sieve_of_eratosthenes(max_num):
        is_prime = [True] * (max_num + 1)
        p = 2
        while (p * p <= max_num):
            if (is_prime[p] == True):
                for i in range(p * p, max_num + 1, p):
                    is_prime[i] = False
            p += 1
        prime_numbers = [p for p in range(2, max_num + 1) if is_prime[p]]
        return prime_numbers

    primes = sieve_of_eratosthenes(n)
    dp = [0] * (n + 1)
    dp[0] = 0
    for i in range(1, n + 1):
        for prime in primes:
            if prime > i:
                break
            dp[i] = max(dp[i], dp[i - prime] + 1)

    result = []
    remaining = n
    while remaining > 0:
        for prime in reversed(primes):
            if prime <= remaining and dp[remaining] == dp[remaining - prime] + 1:
                result.append(prime)
                remaining -= prime
                break

    print(dp[n])
    print(" ".join(map(str, result)))

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    n = int(input().strip())
    bachgold_problem(n)