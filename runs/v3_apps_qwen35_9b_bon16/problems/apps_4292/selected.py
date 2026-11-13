import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    k = int(input_data[1])
    prices = [int(x) for x in input_data[2:2+n]]

    prices.sort()
    result = sum(prices[:k])
    print(result)

if __name__ == "__main__":
    solve()