import sys

def min_coins_to_same_position(n, chips):
    # Count the number of chips at odd and even positions
    odd_count = sum(1 for x in chips if x % 2 == 1)
    even_count = n - odd_count
    
    # The minimum cost will be the smaller count of chips, as we can move all chips to the parity they are not in for free
    return min(odd_count, even_count)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    chips = list(map(int, data[1:]))
    
    result = min_coins_to_same_position(n, chips)
    print(result)

if __name__ == "__main__":
    main()