import sys
from collections import defaultdict
from math import factorial

MOD = 1_000_000_007

def count_permutations(n):
    return factorial(n) % MOD

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    names = data[1:]
    
    # Group names by their starting letter sequence
    groups = defaultdict(list)
    for name in names:
        prefix = ""
        for char in name:
            prefix += char
            groups[prefix].append(name)
    
    # Calculate the number of valid permutations
    result = 1
    for group in groups.values():
        result *= count_permutations(len(group))
        result %= MOD
    
    # Multiply by the number of ways to arrange the groups
    result *= count_permutations(len(groups))
    result %= MOD
    
    print(result)

if __name__ == "__main__":
    main()