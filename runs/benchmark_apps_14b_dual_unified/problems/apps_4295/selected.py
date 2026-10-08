import sys

def main():
    import sys
    def read_ints():
        return map(int, sys.stdin.read().split())
    
    N, K = read_ints()
    result = min(N % K, K - N % K)
    print(result)

if __name__ == "__main__":
    main()