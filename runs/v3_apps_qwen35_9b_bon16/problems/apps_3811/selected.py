import sys

# Increase recursion depth just in case, though we will use an iterative approach.
sys.setrecursionlimit(200000)

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

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

    # We need to find an integer X > 1 such that for every pair (a, b),
    # X divides a OR X divides b.
    # 
    # Strategy:
    # The answer X must be composed of prime factors.
    # For each prime factor p of X, p must satisfy the condition for all pairs.
    # However, checking all primes up to 2*10^9 is impossible.
    #
    # Observation:
    # For a specific pair (a, b), the candidate divisors must come from the factors of a or the factors of b.
    # Specifically, if a solution X exists, then for each pair i, X must share a common factor with either a_i or b_i.
    # Actually, it's stronger: X must divide at least one element. So for pair i, if X divides a_i, then all prime factors of X are among prime factors of a_i.
    #
    # Let's consider the set of all prime factors present in all numbers. This is still too large.
    # But note: if a solution X exists, then for the first pair (a1, b1), X must divide a1 or b1.
    # So X must be a divisor of a1 or a divisor of b1.
    # Since X > 1, X must have at least one prime factor p.
    # If X divides a1, then p divides a1. If X divides b1, then p divides b1.
    # Therefore, any valid X must have all its prime factors drawn from the prime factors of a1 OR the prime factors of b1? 
    # No, that's not strictly true. X could be a composite number where some factors come from a1 and others from b1, as long as X itself divides one of them.
    # Wait, if X divides a1, then ALL prime factors of X must be prime factors of a1.
    # If X divides b1, then ALL prime factors of X must be prime factors of b1.
    # So for the first pair, X must be a divisor of a1 OR a divisor of b1.
    # This implies that X must be formed entirely by prime factors of a1, OR entirely by prime factors of b1.
    # Thus, the set of candidate X's is limited to the divisors of a1 and the divisors of b1.
    # However, checking all divisors is too slow (2*10^9 has many divisors in worst case, but average is low? No, we can't iterate).
    #
    # Correct approach:
    # The candidate X must be a divisor of a1 OR a divisor of b1.
    # But we don't need to check ALL divisors. We can collect all "interesting" numbers.
    # What if we just collect all prime factors of a1 and b1?
    # Let P be the set of all prime factors of a1 and b1 combined.
    # Any valid X must be composed of primes from P? Yes, because if X divides a1, its primes are in a1. If X divides b1, its primes are in b1.
    # So X is composed of primes from (primes(a1) U primes(b1)).
    #
    # But even better:
    # For a fixed candidate X, it must work for ALL pairs.
    # Instead of iterating X, let's think about the constraints on X.
    # For each pair i, X must divide a_i or X must divide b_i.
    # This is equivalent to: X is in the set D(a_i) U D(b_i), where D(n) is the set of divisors of n.
    # We are looking for X > 1 such that X in (intersection over i of (D(a_i) U D(b_i))).
    #
    # Since n is up to 150,000, we cannot compute intersections of sets of divisors directly.
    # However, note that if such an X exists, then for the first pair (a1, b1), X must divide a1 or b1.
    # Let's assume X divides a1. Then X is a divisor of a1.
    # Then we check if this X works for all other pairs.
    # But there are too many divisors.
    #
    # Alternative Insight:
    # If a solution X exists, then for each pair i, gcd(X, a_i) * gcd(X, b_i) >= X? No.
    # The condition is: (X | a_i) or (X | b_i).
    # This is equivalent to: NOT (X does not divide a_i AND X does not divide b_i).
    #
    # Let's reconsider the first pair (a1, b1).
    # X must divide a1 or X must divide b1.
    # Case 1: X divides a1. Then X is a divisor of a1.
    # Case 2: X divides b1. Then X is a divisor of b1.
    #
    # We can iterate over the prime factors of a1 and b1? 
    # No, X doesn't have to be prime. But if X works, then any prime factor p of X also works?
    # If X divides a_i, then p divides a_i. If X divides b_i, then p divides b_i.
    # So if X is a solution, then every prime factor of X is also a solution?
    # Let's verify. Suppose X=6, pairs=(12, 15), (25, 18).
    # Pair 1: 6|12 (ok). Pair 2: 6|18 (ok).
    # Prime factors of 6 are 2 and 3.
    # Check p=2: Pair 1: 2|12 (ok). Pair 2: 2|18 (ok). OK.
    # Check p=3: Pair 1: 3|15 (ok). Pair 2: 3|18 (ok). OK.
    # So yes, if X is a solution, then any prime factor of X is a solution.
    # Therefore, if a solution exists, there exists a PRIME solution.
    # Proof: Let X be a solution. Let p be a prime factor of X. For any pair (a, b), since X|a or X|b, and p|X, then p|a or p|b. So p is a solution.
    #
    # So we only need to find a PRIME p > 1 that satisfies the condition.
    # And from the first pair (a1, b1), any such prime p must divide a1 or b1.
    # So p must be in the set of prime factors of a1 OR in the set of prime factors of b1.
    #
    # Algorithm:
    # 1. Get prime factors of a1 and b1. Let this set be Candidates.
    # 2. For each prime p in Candidates:
    #    Check if p divides at least one element in EVERY pair.
    #    If yes, return p.
    # 3. If no candidate works, return -1.
    #
    # Complexity:
    # - Factorizing a1 and b1: a1, b1 <= 2*10^9. Trial division up to sqrt(2*10^9) ~ 45000 is fast enough.
    # - Number of distinct prime factors for a number <= 2*10^9 is small (at most ~10, since 2*3*5*7*11*13*17*19*23*29 > 2*10^9).
    # - Total candidates is very small (<= 20).
    # - Checking each candidate against N pairs: O(N).
    # - Total complexity: O(sqrt(MAX_VAL) + N * num_factors). This is well within limits for N=150,000.

    def get_prime_factors(num):
        factors = set()
        d = 2
        temp = num
        # Check 2 separately
        if temp % 2 == 0:
            factors.add(2)
            while temp % 2 == 0:
                temp //= 2
        d = 3
        while d * d <= temp:
            if temp % d == 0:
                factors.add(d)
                while temp % d == 0:
                    temp //= d
            d += 2
        if temp > 1:
            factors.add(temp)
        return factors

    # Get candidates from the first pair
    if n == 0:
        print("-1")
        return

    a1, b1 = pairs[0]
    candidates = get_prime_factors(a1) | get_prime_factors(b1)
    
    # Sort candidates to have deterministic output (though any is fine)
    candidate_list = sorted(list(candidates))
    
    for p in candidate_list:
        valid = True
        for i in range(1, n):
            a, b = pairs[i]
            if a % p != 0 and b % p != 0:
                valid = False
                break
        if valid:
            print(p)
            return
            
    print("-1")

if __name__ == "__main__":
    solve()