def main():
    import sys
    input = sys.stdin.read
    data = input().strip()
    N, K = map(int, data.split())
    
    # The minimum value of N after performing the operation
    # is achieved by repeatedly taking the absolute difference
    # with K until N is less than K.
    # This is because once N < K, the absolute difference
    # will only decrease by subtracting K from N.
    
    if N < K:
        print(N)
    else:
        print(abs(N - K))

if __name__ == "__main__":
    main()