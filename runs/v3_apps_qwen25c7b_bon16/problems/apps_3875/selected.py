from sys import stdin, stdout
import math

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a, m):
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError("Modular inverse does not exist")
    else:
        return x % m

def solve():
    N = int(stdin.readline().strip())
    A = list(map(int, stdin.readline().strip().split()))
    
    dp = [0] * (N + 1)
    inv_dp = [0] * (N + 1)
    dp[0] = 1
    inv_dp[0] = 1
    
    MOD = 1000000007
    
    for i in range(1, N + 1):
        dp[i] = sum(dp[j] for j in range(i)) % MOD
        inv_dp[i] = mod_inverse(dp[i], MOD)
    
    result = 0
    for i in range(N):
        result += (dp[i] * inv_dp[N]) % MOD
        result %= MOD
    
    stdout.write(str(result) + '\n')

if __name__ == "__main__":
    solve()