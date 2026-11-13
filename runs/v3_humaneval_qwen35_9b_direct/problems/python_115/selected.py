import math

def max_fill(grid, capacity):
    total_drops = 0
    for well in grid:
        water_units = sum(well)
        if water_units > 0:
            drops_for_well = math.ceil(water_units / capacity)
            total_drops += drops_for_well
    return total_drops