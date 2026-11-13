import math

def max_fill(grid, capacity):
    total_trips = 0
    for well in grid:
        water_units = sum(well)
        trips = math.ceil(water_units / capacity)
        total_trips += trips
    return total_trips