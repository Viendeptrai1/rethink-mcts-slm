import sys
import math

def min_moves_to_reach_N(N):
    # Find the smallest integer k such that k^2 >= N
    k = math.ceil(math.sqrt(N))
    
    # Calculate the minimum number of moves
    moves = k - 1 + (N // k) - 1
    
    return moves

if __name__ == "__main__":
    N = int(sys.stdin.read().strip())
    result = min_moves_to_reach_N(N)
    sys.stdout.write(str(result))