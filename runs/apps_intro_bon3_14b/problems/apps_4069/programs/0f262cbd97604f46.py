import sys

def main():
    import sys
    X, K, D = map(int, sys.stdin.read().split())
    
    # Calculate the maximum possible distance Takahashi can move in K moves
    max_distance = K * D
    
    # Calculate the effective distance after moving as far as possible towards zero
    if X > 0:
        effective_distance = max_distance - X
    else:
        effective_distance = max_distance + X
    
    # The result is the remainder of effective_distance divided by 2D
    result = effective_distance % (2 * D)
    
    # If the result is greater than D, it means we can move back by D to get closer to zero
    if result > D:
        result = 2 * D - result
    
    # Print the minimum possible absolute value of the coordinate of the destination
    print(result)

if __name__ == "__main__":
    main()