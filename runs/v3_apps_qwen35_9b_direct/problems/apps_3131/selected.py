import sys

def solve():
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

    MOD = 1000000007

    a.sort(reverse=True)

    # Precompute factorials and inverse factorials for combinations
    # We need C(n, K-1) for n from K-1 to N-1
    # Max n is N-1, so we need factorials up to N
    max_val = N
    fact = [1] * (max_val + 1)
    inv = [1] * (max_val + 1)
    
    for i in range(1, max_val + 1):
        fact[i] = (fact[i-1] * i) % MOD

    inv[max_val] = pow(fact[max_val], MOD - 2, MOD)
    for i in range(max_val - 1, -1, -1):
        inv[i] = (inv[i+1] * (i + 1)) % MOD

    def nCr_mod(n, r):
        if r < 0 or r > n:
            return 0
        num = fact[n]
        den = (inv[r] * inv[n-r]) % MOD
        return (num * den) % MOD

    total_sum = 0

    # For each key i (0-indexed in sorted array), it is the maximum in a combination
    # if we choose K-1 keys from the remaining N-1-i keys that are smaller or equal.
    # Since the array is sorted descending, keys at indices > i are <= a[i].
    # Number of such keys is (N - 1) - i.
    # We need to choose K-1 from these.
    
    count_smaller = N - 1 - i
    ways = nCr_mod(count_smaller, K - 1)
    
    if ways > 0:
        term = (a[i] * ways) % MOD
        total_sum = (total_sum + term) % MOD

    print(total_sum)

if __name__ == "__main__":
    solve()