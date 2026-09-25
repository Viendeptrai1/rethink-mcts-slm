def max_fill(grid, capacity):
    import math
    
    # Calculate the total amount of water in the grid
    total_water = sum(sum(row) for row in grid)
    
    # Calculate the number of times buckets need to be lowered
    # Each time a bucket is lowered, it can remove 'capacity' units of water
    return math.ceil(total_water / capacity)

# Example usage:
# print(max_fill([[0,0,1,0], [0,1,0,0], [1,1,1,1]], 1))  # Output: 6
# print(max_fill([[0,0,1,1], [0,0,0,0], [1,1,1,1], [0,1,1,1]], 2))  # Output: 5
# print(max_fill([[0,0,0], [0,0,0]], 5))  # Output: 0