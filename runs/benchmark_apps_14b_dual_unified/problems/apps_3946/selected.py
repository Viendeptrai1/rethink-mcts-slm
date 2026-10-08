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
    index += n
    
    total_weight = sum(w)
    
    expected_weights = [0] * n
    
    for i in range(n):
        if a[i] == 1:
            expected_weights[i] = (w[i] + m) * mod_inverse(total_weight, MOD)
        else:
            expected_weights[i] = (w[i] - m) * mod_inverse(total_weight, MOD)
    
    for ew in expected_weights:
        print(ew)

if __name__ == "__main__":
    main()