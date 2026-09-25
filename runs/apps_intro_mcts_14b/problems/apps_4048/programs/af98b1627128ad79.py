import sys
import math

def min_moves_to_reach_N(N):
    # Find the smallest integer i such that i * i >= N
    i = math.ceil(math.sqrt(N))
    # Calculate the minimum number of moves
    moves = i + (N // i) - 2
    return moves

if __name__ == "__main__":
    N = int(sys.stdin.read().strip())
    result = min_moves_to_reach_N(N)
    sys.stdout.write(str(result))