import sys

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def get_prime_factors(num):
    factors = set()
    d = 2
    temp = num
    while d * d <= temp:
        if temp % d == 0:
            factors.add(d)
            while temp % d == 0:
                temp //= d
        d += 1
    if temp > 1:
        factors.add(temp)
    return factors

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    try:
        n = int(next(iterator))
    except StopIteration:
        return

    pairs = []
    for _ in range(n):
        a = int(next(iterator))
        b = int(next(iterator))
        pairs.append((a, b))

    if n == 0:
        print(-1)
        return

    # We will test prime factors of the first element of the first pair
    # If none work, we might need to check other numbers, but the problem guarantees
    # that if a solution exists, there is a prime solution. And if a prime p works,
    # it must divide at least one number in every pair.
    # The strategy: pick a candidate number from the first pair (say a1), get its prime factors.
    # If any of those primes satisfy the condition, return it.
    # If not, try the other number in the first pair (b1).
    # If neither works, then no prime factor from the first pair can be the WCD.
    # However, is it possible that the WCD is a prime that does NOT divide a1 or b1?
    # No, because the WCD must divide at least one number in the FIRST pair.
    # So the WCD must be a factor of a1 or b1. Since we need a prime WCD (or a multiple of one),
    # checking prime factors of a1 and b1 is sufficient. If a composite works, its prime factor also works.
    # So we only need to check primes.

    candidates = []
    a1, b1 = pairs[0]
    candidates.extend(get_prime_factors(a1))
    candidates.extend(get_prime_factors(b1))
    
    # Remove duplicates and sort (optional)
    candidates = sorted(list(set(candidates)))

    for p in candidates:
        valid = True
        for i in range(1, n):
            a, b = pairs[i]
            if a % p != 0 and b % p != 0:
                valid = False
                break
        if valid:
            print(p)
            return

    print(-1)

if __name__ == "__main__":
    solve()