def max_non_participating_items(n, X, prices):
    prices.sort()
    count = 0
    for i in range(n):
        if i + 1 < n and prices[i] + prices[i + 1] > X:
            count += 1
            i += 1  # Skip the next item to avoid using a pair
    return n - count

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    X = int(data[1])
    prices = list(map(int, data[2:n+2]))
    result = max_non_participating_items(n, X, prices)
    print(result)

if __name__ == "__main__":
    main()