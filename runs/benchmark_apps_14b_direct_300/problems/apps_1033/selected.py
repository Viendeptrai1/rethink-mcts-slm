import sys

def min_spots(n, H):
    if H >= n:
        return 1
    if H == 1:
        return n
    k = (n + H - 1) // H
    return 2 * k - 1

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    H = int(data[1])
    print(min_spots(n, H))

if __name__ == "__main__":
    main()