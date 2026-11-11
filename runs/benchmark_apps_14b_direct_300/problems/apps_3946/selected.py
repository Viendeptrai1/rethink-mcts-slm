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
    
    index = 0
    n = int(data[index])
    m = int(data[index + 1])
    index += 2
    
    a = list(map(int, data[index:index + n]))
    index += n
    
    w = list(map(int, data[index:index + n]))
    
    total_weight = sum(w)
    
    numerator = [0] * n
    denominator = [0] * n
    
    for i in range(n):
        numerator[i] = w[i] * (m + 1)
        denominator[i] = total_weight * (m + 1)
        
        if a[i] == 1:
            numerator[i] += m
        else:
            numerator[i] -= m
    
    for i in range(n):
        g = gcd(numerator[i], denominator[i])
        numerator[i] //= g
        denominator[i] //= g
        
        result = (numerator[i] * mod_inverse(denominator[i], MOD)) % MOD
        print(result, end=' ')

if __name__ == "__main__":
    main()