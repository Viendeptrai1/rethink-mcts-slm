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
        possible = True
        
        # Check each power of 2 from highest to lowest
        for power in range(31, -1, -1):
            value = 1 << power
            if value > current_b:
                continue
            
            count_needed = current_b // value
            count_available = coin_counts[value]
            
            if count_needed > count_available:
                possible = False
                break
            
            used_coins += count_needed
            current_b -= count_needed * value
        
        if possible:
            results.append(used_coins)
        else:
            results.append(-1)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()