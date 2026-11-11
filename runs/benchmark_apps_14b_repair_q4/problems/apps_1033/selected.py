import sys

def min_spots(n, H):
    if n <= H:
        return 1
    if H == 1:
        return n
    k = (n - H) // (H - 1)
    r = (n - H) % (H - 1)
    if r == 0:
        return 2 * k + 1
    else:
        return 2 * k + 2

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    H = int(data[1])
    print(min_spots(n, H))

if __name__ == "__main__":
    main()