import sys

def solve():
    x = int(sys.stdin.read().strip())
    balance = 100
    years = 0
    while balance < x:
        balance = (balance * 101) // 100
        years += 1
    print(years)

if __name__ == "__main__":
    solve()