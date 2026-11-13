def max_items_for_offer(n, X, prices):
    prices.sort()
    left, right = 0, n - 1
    while left < right:
        if prices[left] + prices[right] <= X:
            left += 1
        else:
            right -= 1
    return right + 1

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    X = int(data[1])
    prices = list(map(int, data[2:]))
    result = max_items_for_offer(n, X, prices)
    print(result)