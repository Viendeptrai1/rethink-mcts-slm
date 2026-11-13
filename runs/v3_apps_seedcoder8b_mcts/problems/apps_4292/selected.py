def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    K = int(data[1])
    prices = list(map(int, data[2:]))
    
    prices.sort()
    min_total_price = sum(prices[:K])
    
    print(min_total_price)

if __name__ == "__main__":
    main()