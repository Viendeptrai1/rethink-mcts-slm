import sys
from collections import defaultdict

MOD = 1_000_000_007

def count_orderings(N, names):
    # Group names by their prefixes
    prefix_groups = defaultdict(list)
    for name in names:
        for i in range(1, len(name) + 1):
            prefix_groups[name[:i]].append(name)
    
    # Calculate the number of ways to arrange each group
    def factorial(n):
        if n == 0 or n == 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result = (result * i) % MOD
        return result
    
    total_ways = 1
    for group in prefix_groups.values():
        total_ways = (total_ways * factorial(len(group))) % MOD
    
    return total_ways

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    names = data[1:]
    
    result = count_orderings(N, names)
    print(result)

if __name__ == "__main__":
    main()