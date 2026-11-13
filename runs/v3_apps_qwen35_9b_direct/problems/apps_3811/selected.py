import sys
import math

# Increase recursion depth just in case, though we will use iterative approaches
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

    # We need to find an integer x > 1 such that for every pair (a, b),
    # x divides a OR x divides b.
    
    # Strategy:
    # The answer must be a divisor of at least one number in each pair.
    # Consider the set of all prime factors present in the entire input.
    # However, checking all primes up to 2*10^9 is too slow.
    # 
    # Observation:
    # If a solution exists, there is likely a "small" solution or a solution composed of small primes.
    # But actually, the solution doesn't have to be small. For example, if we have pairs (P, 1) and (1, P) where P is large prime, no solution.
    # But if we have (P, Q) and (Q, P), then P and Q are candidates.
    #
    # Let's reconsider the constraints. N <= 150,000. Numbers up to 2*10^9.
    # We cannot iterate over all numbers.
    #
    # Key Insight:
    # If a valid WCD X exists, then for each pair i, X must divide a_i or b_i.
    # This implies that X is a common divisor of the set S_i = {a_i, b_i} for all i? No, that's not right.
    # It means X is in the union of divisors of a_i and divisors of b_i for each i.
    #
    # Let's try a randomized approach or a heuristic based on small primes?
    # No, the answer could be a large prime. Example: (1000000007, 1000000009) and (1000000009, 1000000007). 
    # Wait, if the answer is a large prime P, then P must divide at least one element in EVERY pair.
    # This means P must be a factor of a_i or b_i for all i.
    # So P must be a common factor of the set of numbers {a_1, b_1, a_2, b_2, ...} but with the condition that for each pair, it picks one.
    # Actually, if P is the answer, then P divides a_i OR b_i for all i.
    # This implies that P is a divisor of the GCD of some subset?
    #
    # Let's flip the problem.
    # For a candidate X to be valid, it must satisfy the condition.
    # How to find X?
    # Notice that if X is a solution, then any multiple of X is also a solution?
    # Let's check: If X divides a_i or b_i, does 2X divide a_i or b_i? Not necessarily.
    # Example: Pair (2, 3). X=2 works (divides 2). 2X=4 does not work.
    # So the property is not monotonic in that way.
    #
    # However, if X is a solution, then the prime factors of X must individually satisfy a weaker condition?
    # No.
    #
    # Let's look at the structure again.
    # We need X > 1 such that for all i, (a_i % X == 0) or (b_i % X == 0).
    #
    # Consider the set of all prime factors of all numbers in the input.
    # The number of distinct prime factors for numbers up to 2*10^9 is not too huge if we consider the total count, but individual numbers can have many.
    # However, the total number of distinct prime factors across 150,000 numbers * 2 could be large.
    # But wait, if X is a solution, then X must be composed of primes that appear frequently.
    #
    # Alternative approach:
    # Since N is up to 150,000, maybe we can check small primes first?
    # What if the answer is a large prime?
    # If the answer is a large prime P, then P must divide at least one number in every pair.
    # This means P is a common divisor of the set of "chosen" numbers.
    # But we don't know which one is chosen.
    # However, if P divides a_i or b_i for all i, then P must be a divisor of the GCD of the set of all numbers? No.
    # Example: (2, 3), (3, 2). P=3 works. GCD(2,3,3,2) = 1.
    # But P=3 divides 3 in first pair and 3 in second pair.
    #
    # Let's consider the set of all prime factors of all numbers in the input.
    # If a solution X exists, let p be a prime factor of X.
    # Does p have to satisfy the condition?
    # If X divides a_i, then p divides a_i.
    # So if X is a solution, then for every pair i, p divides a_i or b_i.
    # This means ANY prime factor of a valid WCD is also a valid WCD (if we consider the definition "divides at least one element").
    # Wait, the definition says "arbitrary integer greater than 1".
    # If X is a solution, and p is a prime factor of X, then p divides X.
    # If X divides a_i, then p divides a_i.
    # If X divides b_i, then p divides b_i.
    # So yes, if X is a solution, then any prime factor of X is also a solution.
    # Therefore, if a solution exists, there exists a prime solution.
    # We only need to find a prime P such that for all i, P divides a_i or b_i.
    #
    # So the problem reduces to: Find a prime P such that for all i, P | a_i or P | b_i.
    #
    # How to find such a prime?
    # The prime P must be a factor of at least one number in each pair.
    # This implies that P must be a factor of the GCD of some selection of one number from each pair.
    # But we don't know the selection.
    #
    # However, note that if such a prime P exists, it must be a factor of at least one number in the first pair (a_1, b_1).
    # So P must be in the set of prime factors of a_1 OR in the set of prime factors of b_1.
    # Since we need to check this for ALL pairs, we can iterate over the prime factors of a_1 and b_1.
    # For each candidate prime P from the first pair, we check if it satisfies the condition for all other pairs.
    #
    # Is it guaranteed that the solution is a factor of a_1 or b_1?
    # Yes, because the condition must hold for the first pair as well.
    # So the candidate set for P is the union of prime factors of a_1 and prime factors of b_1.
    #
    # How many prime factors can a number up to 2*10^9 have?
    # The product of the first 10 primes is already > 2*10^9 (2*3*5*7*11*13*17*19*23*29 = 6,469,693,230).
    # So a number has at most 9 distinct prime factors.
    # Total candidates from the first pair is at most 18.
    # For each candidate, we iterate through N pairs.
    # Complexity: 18 * N. With N=150,000, operations ~ 2.7 million, which is well within time limits (usually 1-2 seconds for Python).
    #
    # Algorithm:
    # 1. Read input.
    # 2. Get prime factors of a_1 and b_1.
    # 3. For each unique prime factor P in (factors(a_1) U factors(b_1)):
    #    a. Check if for all i from 1 to n, (a_i % P == 0) or (b_i % P == 0).
    #    b. If yes, print P and exit.
    # 4. If no prime from the first pair works, output -1.
    #
    # Wait, is it possible that the solution is composite but no prime factor of it works?
    # We proved earlier: If X is a solution, and p is a prime factor of X, then p is also a solution.
    # Proof:
    #   Assume X is a solution. Then for all i, X | a_i or X | b_i.
    #   Let p be a prime factor of X.
    #   If X | a_i, then a_i = k*X = k*m*p, so p | a_i.
    #   Similarly if X | b_i, then p | b_i.
    #   So for all i, p | a_i or p | b_i.
    #   Thus p is a solution.
    # So we only need to check primes.
    #
    # Implementation details:
    # - Function to get prime factors of a number up to 2*10^9.
    #   We can trial divide up to sqrt(2*10^9) approx 45000.
    #   If after trial division the number > 1, the remainder is a prime.
    # - Collect unique primes from a_1 and b_1.
    # - Iterate and check.

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

def main():
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
        # Problem says n >= 1, but just in case
        print("-1")
        return

    a1, b1 = pairs[0]
    
    # Get candidate primes from the first pair
    candidates = set()
    candidates.update(get_prime_factors(a1))
    candidates.update(get_prime_factors(b1))
    
    found = False
    result = -1
    
    for p in candidates:
        valid = True
        for i in range(n):
            a, b = pairs[i]
            if a % p != 0 and b % p != 0:
                valid = False
                break
        if valid:
            result = p
            found = True
            break
            
    if found:
        print(result)
    else:
        print("-1")

if __name__ == '__main__':
    main()