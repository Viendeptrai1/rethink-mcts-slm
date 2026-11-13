import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    m = int(input_data[0])
    n = int(input_data[1])
    
    # The expected value of the maximum of n independent uniform variables on [1, m]
    # E[X] = sum_{k=1}^{m} k * P(X = k)
    # P(X = k) = P(X <= k) - P(X <= k-1)
    # P(X <= k) = (k/m)^n
    # So, E[X] = sum_{k=1}^{m} k * ((k/m)^n - ((k-1)/m)^n)
    
    # Alternatively, using the tail sum formula for non-negative integer random variables:
    # E[X] = sum_{k=0}^{m-1} P(X > k)
    # P(X > k) = 1 - P(X <= k) = 1 - (k/m)^n
    # So, E[X] = sum_{k=0}^{m-1} (1 - (k/m)^n)
    #          = m - sum_{k=0}^{m-1} (k/m)^n
    # Note: when k=0, term is 0. So sum from k=1 to m-1.
    
    # Let's use the direct definition sum_{k=1}^{m} k * P(X=k) for clarity and robustness,
    # though the tail sum is slightly more efficient.
    # E[X] = sum_{k=1}^{m} k * ( (k/m)^n - ((k-1)/m)^n )
    #      = (1/m^n) * sum_{k=1}^{m} k * (k^n - (k-1)^n)
    
    # Given constraints m, n <= 10^5, an O(m) loop is acceptable.
    # We need to be careful with floating point precision.
    
    total = 0.0
    m_float = float(m)
    n_float = float(n)
    
    # Precompute powers might be slow if done naively inside loop, but pow(k, n) is O(log n).
    # Total complexity O(m log n). With m=10^5, log n ~ 17, operations ~ 1.7e6, well within time limits.
    
    for k in range(1, m + 1):
        p_k = pow(k, n)
        p_k_minus_1 = pow(k - 1, n)
        prob_k = (p_k - p_k_minus_1) / pow(m, n)
        total += k * prob_k
        
    print(f"{total:.12f}")

if __name__ == "__main__":
    solve()