import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    x1 = int(input_data[0])
    y1 = int(input_data[1])
    x2 = int(input_data[2])
    y2 = int(input_data[3])

    dx = abs(x1 - x2)
    dy = abs(y1 - y2)

    if dx == 0 or dy == 0:
        print(8 + 2 * (dx + dy))
    else:
        print(2 * (dx + dy + 2))

if __name__ == "__main__":
    solve()