def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    coins = list(map(int, data[2:2+n]))
    
    # Find all possible sums that can be made with the coins
    possible_sums = set()
    possible_sums.add(0)
    
    for coin in coins:
        new_sums = set()
        for s in possible_sums:
            new_sums.add(s + coin)
        possible_sums.update(new_sums)
    
    # Find all sums that can be made with the subset of coins that sum to k
    subset_sums = set()
    subset_sums.add(0)
    
    for coin in coins:
        if k - coin in possible_sums:
            new_sums = set()
            for s in subset_sums:
                new_sums.add(s + coin)
            subset_sums.update(new_sums)
    
    # Output the results
    result = sorted(subset_sums)
    print(len(result))
    print(" ".join(map(str, result)))

if __name__ == "__main__":
    main()