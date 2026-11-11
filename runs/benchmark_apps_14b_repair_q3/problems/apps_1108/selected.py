import sys

def main():
    import sys
    n = int(sys.stdin.readline())
    count = 0
    for _ in range(n):
        p, q = map(int, sys.stdin.readline().split())
        if q - p >= 2:
            count += 1
    print(count)

if __name__ == "__main__":
    main()