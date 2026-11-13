import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    N = int(next(iterator))
    K = int(next(iterator))

    prices = []
    for _ in range(N):
        prices.append(int(next(iterator)))

    prices.sort()

    total_price = sum(prices[:K])
    print(total_price)

if __name__ == "__main__":
    solve()