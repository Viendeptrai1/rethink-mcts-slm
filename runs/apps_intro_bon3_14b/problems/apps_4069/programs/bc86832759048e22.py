import sys

def main():
    import sys
    X, K, D = map(int, sys.stdin.read().split())
    
    # Calculate the maximum distance Takahashi can move in K moves
    max_distance = K * D
    
    # Calculate the effective distance after moving as far as possible towards zero
    if X > 0:
        effective_distance = max_distance - (max_distance // (2 * D)) * (2 * D)
    else:
        effective_distance = max_distance - ((max_distance + D) // (2 * D)) * (2 * D)
    
    # Calculate the final position
    final_position = X + effective_distance
    
    # Return the minimum possible absolute value of the coordinate of the destination
    print(abs(final_position))

if __name__ == "__main__":
    main()