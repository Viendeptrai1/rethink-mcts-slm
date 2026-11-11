import sys
from itertools import combinations

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    K = int(data[1])
    a = list(map(int, data[2:]))
    
    total_sum = 0
    for combo in combinations(a, K):
        total_sum += max(combo)
    
    result = total_sum % 1000000007
    print(result)

if __name__ == "__main__":
    main()