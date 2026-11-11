import sys
from math import comb

MOD = 10**9 + 7

def sum_of_partition_weights(n, k, weights):
    total_weight = sum(weights)
    result = 0
    
    for i in range(k):
        binom_coeff = comb(n, i)
        subset_weight = total_weight * (n - i)
        result += binom_coeff * subset_weight
        result %= MOD
    
    return result

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    weights = list(map(int, data[2:]))
    
    print(sum_of_partition_weights(n, k, weights))

if __name__ == "__main__":
    main()