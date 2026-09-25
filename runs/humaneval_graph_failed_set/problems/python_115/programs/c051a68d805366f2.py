def max_fill(grid, bucket_capacity):
    import math
    
    # Check for empty grid
    if not grid or not grid[0]:
        return 0
    
    # Calculate total water units
    total_water_units = sum(sum(well) for well in grid)
    
    # Calculate the number of bucket lowerings needed
    return math.ceil(total_water_units / bucket_capacity)