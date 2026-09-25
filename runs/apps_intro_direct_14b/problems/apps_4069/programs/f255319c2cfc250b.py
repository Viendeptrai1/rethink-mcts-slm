import sys

def main():
    import sys
    X, K, D = map(int, sys.stdin.read().split())
    
    # Calculate the maximum distance Takahashi can travel in K moves
    max_distance = K * D
    
    # Calculate the effective distance after reaching the farthest point in the positive direction
    if X > 0:
        effective_distance = max_distance - X
    else:
        effective_distance = max_distance + X
    
    # If the effective distance is zero or less, the destination is at 0
    if effective_distance <= 0:
        print(0)
        return
    
    # Calculate the remainder of the effective distance divided by 2*D
    remainder = effective_distance % (2 * D)
    
    # The minimum possible absolute value of the coordinate of the destination
    min_abs_value = abs(X - (K - (effective_distance // (2 * D))) * D)
    
    print(min_abs_value)

if __name__ == "__main__":
    main()