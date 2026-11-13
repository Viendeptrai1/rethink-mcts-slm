import sys

def min_spots(n, H):
    if n <= H:
        return n
    else:
        return H + 1

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    H = int(data[1])
    result = min_spots(n, H)
    print(result)