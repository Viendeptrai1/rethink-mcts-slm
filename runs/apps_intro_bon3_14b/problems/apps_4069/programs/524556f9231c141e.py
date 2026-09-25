import sys

def main():
    import sys
    X, K, D = map(int, sys.stdin.read().split())
    
    # Calculate the maximum distance Takahashi can travel in K moves
    max_distance = K * D
    
    # Calculate the effective distance after reaching the farthest point
    effective_distance = abs(X) % D
    
    # Calculate the number of full D moves needed to reach the closest point to zero
    full_moves = (abs(X) - effective_distance) // D
    
    # If the number of full moves is less than K, consider the remaining moves
    if full_moves < K:
        remaining_moves = K - full_moves
        if remaining_moves % 2 == 0:
            # If remaining moves are even, we can return to the same side
            result = effective_distance
        else:
            # If remaining moves are odd, we need to switch sides
            result = min(effective_distance, D - effective_distance)
    else:
        # If no more moves are needed, the result is the effective distance
        result = effective_distance
    
    print(result)

if __name__ == "__main__":
    main()