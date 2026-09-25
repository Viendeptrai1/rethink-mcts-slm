import sys
import math

def min_moves_to_reach_N(N):
    # Find the largest perfect square less than or equal to N
    root = int(math.sqrt(N))
    
    # Calculate the minimum number of moves
    # It's the sum of the coordinates of the square minus 2 (since we start at (1,1))
    min_moves = root + (N // root) - 2
    
    return min_moves

if __name__ == "__main__":
    N = int(sys.stdin.read().strip())
    result = min_moves_to_reach_N(N)
    sys.stdout.write(str(result))