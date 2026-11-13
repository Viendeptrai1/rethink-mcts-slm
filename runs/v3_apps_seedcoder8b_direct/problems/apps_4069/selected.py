def min_possible_absolute_value():
    import sys
    input = sys.stdin.read
    data = input().strip()
    X, K, D = map(int, data.split())
    
    # Calculate the total distance Takahashi can cover in K moves
    total_distance = K * D
    
    # Calculate the new position after K moves
    new_position = X + total_distance
    
    # The minimum possible absolute value of the destination
    # is the minimum of the absolute value of the new position
    # and the absolute value of the new position minus 2*D
    min_abs_value = min(abs(new_position), abs(new_position - 2 * D))
    
    print(min_abs_value)