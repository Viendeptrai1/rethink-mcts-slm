def count_ways(N, M, K):
    MOD = 10**6 + 7
    
    # Function to compute x^y % p using binary exponentiation
    def power(x, y, p):
        res = 1
        x = x % p
        while y > 0:
            if (y & 1) == 1:
                res = (res * x) % p
            y = y >> 1
            x = (x * x) % p
        return res
    
    # Function to compute nCr % p
    def nCr(n, r, p):
        if r > n:
            return 0
        if r == 0 or r == n:
            return 1
        
        # Compute factorial of n, r, and n-r
        fact = [1] * (n + 1)
        for i in range(2, n + 1):
            fact[i] = fact[i - 1] * i % p
        
        # Compute modular inverse of r! and (n-r)!
        inv_r = power(fact[r], p - 2, p)
        inv_nr = power(fact[n - r], p - 2, p)
        
        # Return nCr % p
        return fact[n] * inv_r % p * inv_nr % p
    
    # Calculate the number of ways to take exactly K objects
    result = 0
    for i in range(1, K + 1):
        result = (result + nCr(N, i, MOD) * power(M, i, MOD)) % MOD
    
    return result

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().strip()
    N, M, K = map(int, data.split())
    print(count_ways(N, M, K))