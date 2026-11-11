import sys
from typing import List, Tuple

MOD = 998244353

def count_remaining_sets(N: int, robots: List[Tuple[int, int]]) -> int:
    # Sort robots by their starting position
    robots.sort()
    
    # Create a list to store the end positions of the robots
    end_positions = [x + d for x, d in robots]
    
    # Use a set to keep track of unique end positions
    unique_end_positions = set(end_positions)
    
    # The number of possible sets of robots remaining is 2^(number of unique end positions)
    # because each unique end position can either have a robot or not.
    num_unique_end_positions = len(unique_end_positions)
    result = pow(2, num_unique_end_positions, MOD)
    
    return result

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    robots = []
    index = 1
    for i in range(N):
        x = int(data[index])
        d = int(data[index + 1])
        robots.append((x, d))
        index += 2
    
    result = count_remaining_sets(N, robots)
    print(result)

if __name__ == "__main__":
    main()