from itertools import combinations

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    K = int(data[1])
    values = list(map(int, data[2:]))
    
    total_sum = 0
    mod = 1000000007
    
    for combo in combinations(values, K):
        max_value = max(combo)
        total_sum += max_value
    
    result = total_sum % mod
    print(result)

if __name__ == "__main__":
    main()