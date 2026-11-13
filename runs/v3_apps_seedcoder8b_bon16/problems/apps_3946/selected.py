import sys
from math import gcd

MOD = 998244353

def mod_inverse(a, mod):
    return pow(a, mod - 2, mod)

def main():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    
    a = [int(data[2 + i]) for i in range(n)]
    w = [int(data[2 + n + i]) for i in range(n)]
    
    total_weight = sum(w)
    
    # Calculate final weights after m visits
    for _ in range(m):
        for i in range(n):
            if a[i] == 1:  # Nauuo likes the picture
                w[i] += 1
            else:  # Nauuo does not like the picture
                w[i] -= 1
    
    # Calculate expected weights
    r = []
    for i in range(n):
        q = w[i]
        p = total_weight
        g = gcd(q, p)
        r_i = (q // g) % MOD
        r.append(r_i)
    
    # Output the result
    print(" ".join(map(str, r)))

if __name__ == "__main__":
    main()