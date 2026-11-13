def max_fill(grid, capacity):
    import math
    total_raises = 0
    for well in grid:
        total_water_units = sum(well)
        if total_water_units == 0:
            continue
        raises = math.ceil(total_water_units / capacity)
        total_raises += raises
    return total_raises