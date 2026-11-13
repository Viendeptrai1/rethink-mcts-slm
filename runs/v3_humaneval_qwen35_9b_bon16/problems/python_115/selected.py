import math

def max_fill(grid, capacity):
    total_dips = 0
    for well in grid:
        water_units = sum(well)
        if water_units > 0:
            total_dips += math.ceil(water_units / capacity)
    return total_dips