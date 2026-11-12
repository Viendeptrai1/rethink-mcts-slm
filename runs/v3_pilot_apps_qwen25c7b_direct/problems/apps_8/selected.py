def min_extra_tiles(tiles):
    from collections import Counter
    
    # Count the occurrences of each tile
    tile_count = Counter(tiles)
    
    # Check for koutsu
    koutsu_needed = 0
    for count in tile_count.values():
        if count % 3 != 0:
            koutsu_needed += 1
    
    # Check for shuntsu
    def is_shuntsu(tiles):
        return len(set(tiles)) == 3 and abs(int(tiles[0][0]) - int(tiles[1][0])) == 1 and abs(int(tiles[1][0]) - int(tiles[2][0])) == 1
    
    shuntsu_needed = 0
    for i in range(3):
        for j in range(i+1, 3):
            for k in range(j+1, 3):
                if is_shuntsu([tiles[i], tiles[j], tiles[k]]):
                    shuntsu_needed += 1
                    break
            else:
                continue
            break
    
    # Calculate the minimum number of extra tiles needed
    return max(koutsu_needed, shuntsu_needed)

# Example usage
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    result = min_extra_tiles(data)
    print(result)