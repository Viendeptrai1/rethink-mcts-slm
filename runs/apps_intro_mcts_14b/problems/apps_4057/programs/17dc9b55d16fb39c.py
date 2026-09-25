import sys

def min_pockets(n, coins):
    # Find the unique values among the coins
    unique_values = set(coins)
    # The minimum number of pockets needed is equal to the number of unique values
    return len(unique_values)

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    coins = list(map(int, data[1:]))
    
    result = min_pockets(n, coins)
    print(result)