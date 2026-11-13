def main():
    import sys
    input = sys.stdin.read
    data = input().strip()
    N, K = map(int, data.split())
    
    # The minimum value of N after performing the operation
    # is achieved by repeatedly taking the absolute difference
    # with K until N is less than K.
    while N >= K:
        N = abs(N - K)
    
    print(N)

if __name__ == "__main__":
    main()