from itertools import combinations

def find_possible_sums(n, k, coins):
    # Find all subsets of coins that sum up to k
    valid_subsets = []
    for r in range(1, n + 1):
        for subset in combinations(coins, r):
            if sum(subset) == k:
                valid_subsets.append(subset)
    
    # Collect all possible sums from these subsets
    possible_sums = set()
    for subset in valid_subsets:
        for r in range(len(subset) + 1):
            for combo in combinations(subset, r):
                possible_sums.add(sum(combo))
    
    # Convert to sorted list
    possible_sums = sorted(list(possible_sums))
    
    return possible_sums

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    coins = list(map(int, data[2:]))
    
    possible_sums = find_possible_sums(n, k, coins)
    
    print(len(possible_sums))
    print(" ".join(map(str, possible_sums)))

if __name__ == "__main__":
    main()