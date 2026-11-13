from typing import List
import math

def max_revenue(N: int, S: List[int]) -> int:
    def count_distinct_prime_factors(x: int) -> int:
        factors = set()
        # Check for number of 2s
        while x % 2 == 0:
            factors.add(2)
            x //= 2
        # Check for other primes
        for i in range(3, int(math.sqrt(x)) + 1, 2):
            while x % i == 0:
                factors.add(i)
                x //= i
        if x > 2:
            factors.add(x)
        return len(factors)
    
    total_sum = sum(S)
    max_revenue = 0
    
    for i in range(1 << N):
        current_sum = 0
        for j in range(N):
            if i & (1 << j):
                current_sum += S[j]
        max_revenue = max(max_revenue, count_distinct_prime_factors(current_sum))
    
    return max_revenue

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    N = int(data[0])
    S = list(map(int, data[1:]))
    print(max_revenue(N, S))