def max_fill(grid, capacity):
    total_bucket_lowers = 0
    for row in grid:
        total_water_units = sum(row)
        bucket_lowers_for_well = (total_water_units + capacity - 1) // capacity
        total_bucket_lowers += bucket_lowers_for_well
    return total_bucket_lowers