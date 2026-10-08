import sys
from typing import List, Tuple

MOD = 998244353

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    points = [(int(data[2*i+1]), int(data[2*i+2])) for i in range(N)]
    
    # Sort points by x-coordinate
    points.sort()
    
    # Calculate the contribution of each point
    total_contribution = 0
    
    for i in range(N):
        # Number of points to the left of the current point
        left_count = i
        # Number of points to the right of the current point
        right_count = N - i - 1
        
        # Contribution of the current point
        contribution = (left_count + 1) * (right_count + 1)
        
        total_contribution += contribution
    
    # Print the result modulo 998244353
    print(total_contribution % MOD)

if __name__ == "__main__":
    main()