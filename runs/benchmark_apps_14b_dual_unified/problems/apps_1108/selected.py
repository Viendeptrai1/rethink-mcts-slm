import sys

def main():
    import sys
    n = int(sys.stdin.readline().strip())
    count = 0
    for _ in range(n):
        pi, qi = map(int, sys.stdin.readline().strip().split())
        if qi - pi >= 2:
            count += 1
    print(count)

if __name__ == "__main__":
    main()