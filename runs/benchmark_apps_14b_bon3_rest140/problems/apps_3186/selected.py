import sys
from math import comb

MOD = 10**6 + 7

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    M = int(data[1])
    K = int(data[2])
    
    result = 0
    for i in range(max(0, K - M), min(N, K) + 1):
        result = (result + comb(N, i) * comb(M, K - i)) % MOD
    
    print(result)

if __name__ == "__main__":
    main()