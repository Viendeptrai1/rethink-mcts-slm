def max_fill(grid, capacity):
    total_buckets = 0
    for well in grid:
        water_units = sum(well)
        total_buckets += math.ceil(water_units / capacity)
    return total_buckets