import sys
from math import comb

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    K = int(data[1])
    a = list(map(int, data[2:]))
    
    MOD = 1000000007
    
    a.sort()
    
    result = 0
    
    for i in range(N - 1, K - 2, -1):
        result = (result + a[i] * comb(i, K - 1)) % MOD
    
    print(result)

if __name__ == "__main__":
    main()