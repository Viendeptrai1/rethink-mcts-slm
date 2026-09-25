import sys
from collections import Counter

def min_pockets(n, coins):
    # Count the frequency of each coin value
    coin_count = Counter(coins)
    # The minimum number of pockets needed is the maximum frequency of any coin value
    return max(coin_count.values())

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    coins = list(map(int, data[1:]))
    
    result = min_pockets(n, coins)
    print(result)