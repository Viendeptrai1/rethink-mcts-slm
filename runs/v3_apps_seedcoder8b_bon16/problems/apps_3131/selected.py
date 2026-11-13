import sys
from itertools import combinations

def piano_combinations(N, K, values):
    MOD = 1000000007
    values.sort(reverse=True)
    total_sum = 0
    
    for combo in combinations(values, K):
        total_sum = (total_sum + combo[0]) % MOD
        
    print(total_sum)

def main():
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    K = int(data[1])
    values = list(map(int, data[2:2+N]))
    
    piano_combinations(N, K, values)

if __name__ == "__main__":
    main()