import sys
from collections import defaultdict

MOD = 1_000_000_007

def count_orderings(N, names):
    # Group names by their prefixes
    prefix_groups = defaultdict(list)
    for name in names:
        for i in range(1, len(name) + 1):
            prefix_groups[name[:i]].append(name)
    
    # Calculate the number of valid permutations for each group
    def count_permutations(group):
        if len(group) <= 1:
            return 1
        count = 1
        for i in range(1, len(group)):
            count = (count * (i + 1)) % MOD
        return count
    
    total_count = 1
    for group in prefix_groups.values():
        total_count = (total_count * count_permutations(group)) % MOD
    
    return total_count

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