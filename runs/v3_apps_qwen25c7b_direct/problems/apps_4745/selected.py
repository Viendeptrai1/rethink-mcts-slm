def max_items_for_offer(n, X, prices):
    prices.sort()
    count = 0
    i = 0
    while i < n - 1:
        if prices[i] + prices[i + 1] <= X:
            break
        count += 2
        i += 2
    if i == n - 1:
        count += 1
    return count

# Example usage:
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
X = int(data[1])
prices = list(map(int, data[2:]))

result = max_items_for_offer(n, X, prices)
print(result)