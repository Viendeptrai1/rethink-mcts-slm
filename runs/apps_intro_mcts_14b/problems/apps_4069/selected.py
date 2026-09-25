import sys

def main():
    import sys
    X, K, D = map(int, sys.stdin.read().split())
    
    # Calculate the maximum possible reduction in absolute value
    max_reduction = K * D
    
    # Calculate the new position after maximum reduction
    new_position = X % D
    
    # If the new position is greater than half of D, we can reduce it further
    if new_position > D // 2:
        new_position = D - new_position
    
    # The minimum possible absolute value of the coordinate of the destination
    min_abs_value = abs(new_position)
    
    sys.stdout.write(str(min_abs_value))

if __name__ == "__main__":
    main()