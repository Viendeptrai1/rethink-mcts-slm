import sys

def solve():
    input_data = sys.stdin.read().strip()
    if not input_data:
        return
    n, h, v = map(int, input_data.split())
    piece1 = h * v
    piece2 = h * (n - v)
    piece3 = (n - h) * v
    piece4 = (n - h) * (n - v)
    max_area = max(piece1, piece2, piece3, piece4)
    volume = max_area * 4
    print(volume)

if __name__ == "__main__":
    solve()