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
    coin_counter = Counter()
    for coin in coins:
        coin_counter[coin] += 1
    
    results = []
    
    for b in queries:
        if b == 0:
            results.append(0)
            continue
        
        current_value = b
        num_coins = 0
        
        # Try to use the largest available power of 2 first
        for power in range(31, -1, -1):
            coin_value = 1 << power
            if coin_value > current_value:
                continue
            
            # Determine how many of this coin we can use
            max_coins = min(current_value // coin_value, coin_counter[coin_value])
            current_value -= max_coins * coin_value
            num_coins += max_coins
            
            if current_value == 0:
                break
        
        if current_value == 0:
            results.append(num_coins)
        else:
            results.append(-1)
    
    print("\n".join(map(str, results)))

if __name__ == "__main__":
    main()