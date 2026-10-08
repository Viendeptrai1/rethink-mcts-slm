import sys

def min_spots(n, H):
    if H >= n:
        return 1
    if H == 1:
        return n
    total = 0
    spots = 0
    current_height = H
    while total < n:
        total += current_height
        spots += 1
        if current_height > 1:
            current_height -= 1
        else:
            current_height = H
    return spots

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    H = int(data[1])
    print(min_spots(n, H))

if __name__ == "__main__":
    main()