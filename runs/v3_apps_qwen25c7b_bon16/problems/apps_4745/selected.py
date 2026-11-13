def max_marked_items(n, X, prices):
    prices.sort()
    count = 0
    i, j = 0, n - 1
    while i < j:
        if prices[i] + prices[j] <= X:
            i += 1
        else:
            count += 1
            j -= 1
    return count + (j >= 0)

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
X = int(data[1])
prices = list(map(int, data[2:]))

# Print the result
print(max_marked_items(n, X, prices))