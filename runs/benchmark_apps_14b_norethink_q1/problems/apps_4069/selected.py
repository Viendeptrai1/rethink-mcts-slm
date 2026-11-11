import sys

def main():
    import sys
    def readints():
        return list(map(int, sys.stdin.read().split()))
    
    X, K, D = readints()
    
    # Calculate the maximum distance Takahashi can travel in K moves
    max_distance = K * D
    
    # Calculate the remainder when X is divided by D
    remainder = abs(X) % D
    
    # The minimum possible absolute value of the coordinate of the destination
    min_abs_value = min(remainder, max_distance - remainder)
    
    print(min_abs_value)

if __name__ == "__main__":
    main()