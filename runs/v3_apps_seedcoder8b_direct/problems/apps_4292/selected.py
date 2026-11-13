def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    K = int(data[1])
    prices = list(map(int, data[2:]))
    
    # Sort the prices in ascending order
    prices.sort()
    
    # Calculate the minimum total price by summing the first K prices
    min_total_price = sum(prices[:K])
    
    # Print the result
    print(min_total_price)

if __name__ == "__main__":
    main()