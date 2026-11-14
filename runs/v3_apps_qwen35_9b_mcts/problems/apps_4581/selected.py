import sys

def solve():
    s = sys.stdin.read().strip()
    count = s.count('o')
    price = 700 + 100 * count
    print(price)

if __name__ == "__main__":
    solve()