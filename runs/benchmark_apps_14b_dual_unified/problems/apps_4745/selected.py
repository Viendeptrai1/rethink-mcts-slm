import sys

def max_items_without_horn(n, X, prices):
    prices.sort()
    left = 0
    right = n - 1
    count = 0
    
    while left <= right:
        if prices[left] + prices[right] > X:
            right -= 1
        else:
            count += 1
            left += 1
            right -= 1
    
    return count

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    X = int(data[1])
    prices = list(map(int, data[2:]))
    
    result = max_items_without_horn(n, X, prices)
    print(result)