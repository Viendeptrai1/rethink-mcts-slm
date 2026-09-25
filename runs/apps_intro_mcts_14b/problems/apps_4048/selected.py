import sys
import math

def min_moves_to_reach_N(N):
    min_sum = float('inf')
    for i in range(1, int(math.sqrt(N)) + 1):
        if N % i == 0:
            j = N // i
            min_sum = min(min_sum, i + j - 2)
    return min_sum

if __name__ == "__main__":
    N = int(sys.stdin.read().strip())
    result = min_moves_to_reach_N(N)
    sys.stdout.write(str(result))