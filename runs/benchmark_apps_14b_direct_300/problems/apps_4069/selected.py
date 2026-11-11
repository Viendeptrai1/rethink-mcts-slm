import sys

def main():
    import sys
    def readints():
        return list(map(int, sys.stdin.read().split()))
    
    X, K, D = readints()
    
    # Calculate the maximum distance Takahashi can travel in K moves
    max_distance = K * D
    
    # Calculate the effective distance after reaching the farthest point
    if X > 0:
        effective_distance = max_distance - X
    else:
        effective_distance = max_distance + X
    
    # If the effective distance is less than D, Takahashi can reach the origin
    if effective_distance < D:
        print(0)
    else:
        # Otherwise, calculate the remainder of the effective distance divided by D
        remainder = effective_distance % D
        # The minimum possible absolute value is the minimum of the remainder and D - remainder
        print(min(remainder, D - remainder))

if __name__ == "__main__":
    main()