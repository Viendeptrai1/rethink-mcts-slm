import sys
import math

def min_moves_to_reach_N(N):
    # Find the smallest integer k such that k * (k + 1) / 2 >= N
    k = math.ceil((-1 + math.sqrt(1 + 8 * N)) / 2)
    return k - 1

if __name__ == "__main__":
    N = int(sys.stdin.read().strip())
    result = min_moves_to_reach_N(N)
    sys.stdout.write(str(result))