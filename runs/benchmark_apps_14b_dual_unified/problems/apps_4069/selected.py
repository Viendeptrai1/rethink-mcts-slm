import sys

def main():
    import sys
    def read_ints():
        return map(int, sys.stdin.read().split())
    
    X, K, D = read_ints()
    
    # Calculate the maximum possible position after K moves
    max_position = X + K * D
    
    # Calculate the minimum possible position after K moves
    min_position = X - K * D
    
    # Calculate the distance from the origin
    distance_from_origin = abs(X)
    
    # If K * D is greater than or equal to the distance from the origin
    if K * D >= distance_from_origin:
        # The minimum possible absolute value of the coordinate of the destination
        # is the remainder of the distance from the origin divided by D
        result = distance_from_origin % D
    else:
        # Otherwise, calculate the effective number of moves left after reaching
        # the closest point to the origin
        remaining_moves = K - (distance_from_origin // D)
        
        # If the remaining number of moves is even, Takahashi can end up at the origin
        if remaining_moves % 2 == 0:
            result = 0
        else:
            # If the remaining number of moves is odd, Takahashi will be at a distance
            # of D from the origin
            result = D - (distance_from_origin % D)
    
    print(result)

if __name__ == "__main__":
    main()