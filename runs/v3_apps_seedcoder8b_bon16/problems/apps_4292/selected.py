def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    K = int(data[1])
    prices = list(map(int, data[2:]))
    
    # Sort the prices
    prices.sort()
    
    # Calculate the minimum possible total price of K different fruits
    min_total_price = sum(prices[:K])
    
    # Output the result
    print(min_total_price)

if __name__ == "__main__":
    main()