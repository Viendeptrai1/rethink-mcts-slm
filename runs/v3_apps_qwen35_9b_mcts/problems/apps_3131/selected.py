import sys

# Increase recursion depth just in case, though we use iterative approach
sys.setrecursionlimit(200000)

MOD = 1000000007

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        K = int(next(iterator))
        a = []
        for _ in range(N):
            a.append(int(next(iterator)))
    except StopIteration:
        return

    # If K is 1, the answer is simply the sum of all elements
    if K == 1:
        total = sum(a) % MOD
        print(total)
        return

    # Sort the array in descending order
    a.sort(reverse=True)

    # Precompute factorials and inverse factorials for combinations
    # We need combinations C(n, k) where n can be up to N-1
    # Max n needed is N-1, max k needed is K-1 (since we choose K-1 from remaining)
    
    max_n = N
    fact = [1] * (max_n + 1)
    inv = [1] * (max_n + 1)
    
    for i in range(1, max_n + 1):
        fact[i] = (fact[i-1] * i) % MOD
    
    # Fermat's Little Theorem for modular inverse since MOD is prime
    inv[max_n] = pow(fact[max_n], MOD - 2, MOD)
    for i in range(max_n - 1, -1, -1):
        inv[i] = (inv[i+1] * (i + 1)) % MOD

    def nCr_mod(n, r):
        if r < 0 or r > n:
            return 0
        num = fact[n]
        den = (inv[r] * inv[n-r]) % MOD
        return (num * den) % MOD

    total_sum = 0

    # Iterate through each element. After sorting descending:
    # a[i] is the maximum in any subset of size K that includes a[i]
    # and K-1 elements chosen from the elements after index i (which are smaller or equal).
    # The number of such subsets is C(N - 1 - i, K - 1).
    
    for i in range(N):
        # Number of elements available to choose from after index i
        remaining = N - 1 - i
        
        # We need to choose K-1 from these remaining elements
        if remaining >= K - 1:
            count = nCr_mod(remaining, K - 1)
            term = (a[i] * count) % MOD
            total_sum = (total_sum + term) % MOD

    print(total_sum)

if __name__ == "__main__":
    solve()