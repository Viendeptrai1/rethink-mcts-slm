from collections import Counter

def min_tiles_to_draw(tiles):
    # Count the occurrences of each tile
    tile_count = Counter(tiles)
    
    # Check for existing mentsu
    def has_mentsu():
        for i in range(1, 10):
            if tile_count[f'{i}m'] >= 3 or tile_count[f'{i}p'] >= 3 or tile_count[f'{i}s'] >= 3:
                return True
            if i <= 7 and tile_count[f'{i}m'] >= 1 and tile_count[f'{i+1}m'] >= 1 and tile_count[f'{i+2}m'] >= 1:
                return True
            if i <= 7 and tile_count[f'{i}p'] >= 1 and tile_count[f'{i+1}p'] >= 1 and tile_count[f'{i+2}p'] >= 1:
                return True
            if i <= 7 and tile_count[f'{i}s'] >= 1 and tile_count[f'{i+1}s'] >= 1 and tile_count[f'{i+2}s'] >= 1:
                return True
        return False
    
    # If there is already a mentsu, no need to draw any tiles
    if has_mentsu():
        return 0
    
    # Try drawing one tile at a time and check if a mentsu can be formed
    for i in range(1, 10):
        for suit in 'mps':
            new_tile = f'{i}{suit}'
            tile_count[new_tile] += 1
            if has_mentsu():
                return 1
            tile_count[new_tile] -= 1
    
    # If no mentsu can be formed with one additional tile, draw two tiles
    return 2

# Read input
tiles = input().split()

# Output the result
print(min_tiles_to_draw(tiles))