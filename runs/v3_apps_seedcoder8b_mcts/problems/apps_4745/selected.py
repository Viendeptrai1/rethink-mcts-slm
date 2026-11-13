def max_items_for_offer(n, X, prices):
    prices.sort()
    left, right = 0, n - 1
    count = 0

    while left < right:
        if prices[left] + prices[right] > X:
            right -= 1
        else:
            count += 2
            left += 1
            right -= 1

    return count

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    X = int(data[1])
    prices = list(map(int, data[2:2+n]))
    
    result = max_items_for_offer(n, X, prices)
    print(result)