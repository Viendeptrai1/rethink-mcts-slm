import sys

def main():
    import sys
    N, K = map(int, sys.stdin.read().split())
    print(min(N % K, K - N % K))

if __name__ == "__main__":
    main()