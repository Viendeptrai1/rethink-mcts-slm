import sys

def main():
    import sys
    N, K = map(int, sys.stdin.read().split())
    if N == K:
        print(0)
    elif N < K:
        print(K - N)
    else:
        # If N > K, we need to find the minimum value of |N - m*K| for some integer m
        # This is equivalent to finding the remainder of N divided by K
        print(N % K)

if __name__ == "__main__":
    main()