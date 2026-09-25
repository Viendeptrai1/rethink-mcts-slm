import sys
import math

def min_moves_to_reach_N(N):
    # Find the smallest factor pair (i, j) such that i * j = N
    # We start with i = 1 and increase i until i * i >= N
    i = 1
    while i * i < N:
        if N % i == 0:
            j = N // i
            return i + j - 2
        i += 1
    # If i * i == N, then the optimal path is to go to (i, i)
    return 2 * i - 2

def main():
    import sys
    N = int(sys.stdin.read().strip())
    result = min_moves_to_reach_N(N)
    sys.stdout.write(str(result))

if __name__ == "__main__":
    main()