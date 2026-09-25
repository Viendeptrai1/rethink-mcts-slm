import sys

def min_coins_to_same_coordinate(n, chips):
    # Count the number of chips at even and odd positions
    even_count = sum(1 for x in chips if x % 2 == 0)
    odd_count = n - even_count
    
    # The minimum cost will be the smaller count of even or odd chips
    return min(even_count, odd_count)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    chips = list(map(int, data[1:]))
    
    result = min_coins_to_same_coordinate(n, chips)
    print(result)

if __name__ == "__main__":
    main()