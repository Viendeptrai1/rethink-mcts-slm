import sys
from collections import Counter

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    q = int(data[1])
    
    coins = list(map(int, data[2:2+n]))
    queries = list(map(int, data[2+n:]))
    
    # Count the occurrences of each power of 2 in the coins
    coin_counts = Counter()
    for coin in coins:
        coin_counts[coin] += 1
    
    results = []
    
    for b in queries:
        if b == 0:
            results.append(0)
            continue
        
        current_b = b
        used_coins = 0
        
        # Try to use the largest possible coins first
        for exp in range(31, -1, -1):
            coin_value = 1 << exp
            if coin_value > current_b:
                continue
            
            needed_coins = min(current_b // coin_value, coin_counts[coin_value])
            used_coins += needed_coins
            current_b -= needed_coins * coin_value
        
        if current_b == 0:
            results.append(used_coins)
        else:
            results.append(-1)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()