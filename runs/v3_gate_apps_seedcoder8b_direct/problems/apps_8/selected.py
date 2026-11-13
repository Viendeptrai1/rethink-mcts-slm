def min_tiles_to_draw(tiles):
    # Parse the input tiles
    tile_numbers = [int(tile[0]) for tile in tiles]
    tile_suits = [tile[1] for tile in tiles]

    # Check for koutsu (three identical tiles)
    if len(set(tile_numbers)) == 1:
        return 0

    # Check for shuntsu (three sequential tiles of the same suit)
    tile_numbers_sorted = sorted(tile_numbers)
    if tile_numbers_sorted[0] + 1 == tile_numbers_sorted[1] and tile_numbers_sorted[1] + 1 == tile_numbers_sorted[2]:
        return 0

    # Check if we can form a shuntsu by drawing one tile
    for suit in set(tile_suits):
        # Check for possible shuntsu within the same suit
        for i in range(1, 10):
            if i in tile_numbers:
                if (i - 1 in tile_numbers or i + 1 in tile_numbers) and (i + 2 in tile_numbers or i - 2 in tile_numbers):
                    return 1

    # If no koutsu or shuntsu, we need to draw at least one tile
    return 1

# Read input
import sys
input = sys.stdin.read
tiles = input().strip().split()
print(min_tiles_to_draw(tiles))