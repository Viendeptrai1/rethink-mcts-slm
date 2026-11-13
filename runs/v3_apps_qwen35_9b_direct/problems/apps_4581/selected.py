import sys

def solve():
    s = sys.stdin.read().strip()
    base_price = 700
    topping_count = 0
    for char in s:
        if char == 'o':
            topping_count += 1
    total_price = base_price + topping_count * 100
    print(total_price)

if __name__ == "__main__":
    solve()