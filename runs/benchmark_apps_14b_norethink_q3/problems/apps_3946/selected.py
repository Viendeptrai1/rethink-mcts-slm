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
    
    # Calculate the expected weight change for each picture
    expected_weight_change = [0] * n
    for i in range(n):
        if a[i] == 1:
            expected_weight_change[i] = (m + 1) / (total_weight + m)
        else:
            expected_weight_change[i] = (m - 1) / (total_weight + m)
    
    # Calculate the final expected weights
    final_weights = [int((w[i] + expected_weight_change[i] * m) * MOD) % MOD for i in range(n)]
    
    # Print the results
    for weight in final_weights:
        print(weight)

if __name__ == "__main__":
    main()