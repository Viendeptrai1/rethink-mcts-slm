import sys
from collections import Counter

def main():
    import sys
    from collections import Counter
    
    # Read input
    n = int(sys.stdin.readline())
    coins = list(map(int, sys.stdin.readline().split()))
    
    # Count the frequency of each coin value
    coin_counts = Counter(coins)
    
    # The minimum number of pockets needed is the maximum frequency of any coin value
    min_pockets = max(coin_counts.values())
    
    # Print the result
    print(min_pockets)

if __name__ == "__main__":
    main()