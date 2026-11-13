import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    m = int(input_data[0])
    n = int(input_data[1])

    # Probability that max <= k is (k/m)^n
    # E[X] = sum_{k=1}^{m} P(X >= k)
    # P(X >= k) = 1 - P(X < k) = 1 - ((k-1)/m)^n
    result = 0.0
    base = 1.0 / m

    # We compute sum_{k=1}^{m} (1 - ((k-1)/m)^n)
    # = m - sum_{k=1}^{m} ((k-1)/m)^n
    # = m - sum_{j=0}^{m-1} (j/m)^n
    # Note: for j=0, term is 0 unless n=0 (but n>=1), so we can start from j=1
    
    total_sub = 0.0
    inv_m_pow_n = pow(base, n)
    
    # We can compute powers iteratively to avoid repeated pow calls
    # current_val = (j/m)^n
    # next_val = ((j+1)/m)^n = (j/m)^n * ((j+1)/j)^n ? Not efficient.
    # Better: compute (j/m)^n directly using pow, it's O(log n) and m is 10^5, total ops ~10^5 * log(10^5) which is fine.
    
    for j in range(1, m):
        total_sub += pow(j / m, n)
    
    result = m - total_sub
    print(f"{result:.12f}")

if __name__ == "__main__":
    solve()