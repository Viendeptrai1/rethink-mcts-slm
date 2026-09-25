def max_fill(grid, capacity):
    import math
    total_drops = 0
    for row in grid:
        water_units = sum(row)
        total_drops += math.ceil(water_units / capacity)
    return total_drops