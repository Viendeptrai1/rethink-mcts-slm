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
    
    # Process each query
    results = []
    for b in queries:
        if b == 0:
            results.append(0)
            continue
        
        current_b = b
        used_coins = 0
        
        # Try to use the largest possible coin that does not exceed the remaining value
        for power in range(31, -1, -1):
            coin_value = 1 << power
            if coin_value > current_b:
                continue
            
            max_coins_needed = current_b // coin_value
            available_coins = coin_counter[coin_value]
            
            if available_coins >= max_coins_needed:
                used_coins += max_coins_needed
                current_b -= max_coins_needed * coin_value
            else:
                used_coins += available_coins
                current_b -= available_coins * coin_value
        
        if current_b == 0:
            results.append(used_coins)
        else:
            results.append(-1)
    
    # Print the results
    for result in results:
        print(result)

if __name__ == "__main__":
    main()