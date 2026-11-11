import sys

def max_items_without_horn(n, X, prices):
    prices.sort()
    selected = []
    
    for price in prices:
        valid = True
        for s in selected:
            if s + price > X:
                valid = False
                break
        if valid:
            selected.append(price)
    
    return len(selected)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    X = int(data[1])
    prices = list(map(int, data[2:]))
    
    result = max_items_without_horn(n, X, prices)
    print(result)

if __name__ == "__main__":
    main()