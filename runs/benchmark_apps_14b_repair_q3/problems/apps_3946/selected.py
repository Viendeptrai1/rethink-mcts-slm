import sys
from math import gcd

MOD = 998244353

def mod_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    if m == 1:
        return 0
    while a > 1:
        # q is quotient
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    # Make x1 positive
    if x1 < 0:
        x1 += m0
    return x1

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    a = list(map(int, data[2:2+n]))
    w = list(map(int, data[2+n:2+2*n]))
    
    total_weight = sum(w)
    
    # Calculate the expected weight for each picture
    expected_weights = []
    for i in range(n):
        numerator = (w[i] + m * a[i]) * pow(total_weight + m, MOD - 2, MOD)
        denominator = total_weight + m
        gcd_value = gcd(numerator, denominator)
        numerator //= gcd_value
        denominator //= gcd_value
        result = (numerator * mod_inverse(denominator, MOD)) % MOD
        expected_weights.append(result)
    
    print(' '.join(map(str, expected_weights)))

if __name__ == "__main__":
    main()