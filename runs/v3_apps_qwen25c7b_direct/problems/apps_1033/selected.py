import sys

def min_spots(n, H):
    if n <= H:
        return 1
    elif n == H + 1:
        return 2
    else:
        return 3

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    H = int(data[1])
    result = min_spots(n, H)
    print(result)