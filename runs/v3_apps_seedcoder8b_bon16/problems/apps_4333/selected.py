import sys

def restore_square_coordinates(x1, y1, x2, y2):
    if x1 == x2:
        x3 = x1 + (y2 - y1)
        x4 = x2 + (y2 - y1)
        y3 = y2 - (x2 - x1)
        y4 = y1 - (x2 - x1)
    else:
        x3 = x2 - (y2 - y1)
        x4 = x1 - (y2 - y1)
        y3 = y2 + (x2 - x1)
        y4 = y1 + (x2 - x1)
    return x3, y3, x4, y4

if __name__ == "__main__":
    x1, y1, x2, y2 = map(int, sys.stdin.readline().split())
    result = restore_square_coordinates(x1, y1, x2, y2)
    print(*result)