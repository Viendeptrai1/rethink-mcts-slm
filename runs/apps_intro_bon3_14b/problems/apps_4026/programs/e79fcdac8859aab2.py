import sys

def can_construct_symmetric_square(n, m, tiles):
    # Check if m is odd, if so, it's impossible to construct a symmetric matrix
    if m % 2 != 0:
        return "NO"
    
    # Create a dictionary to store the frequency of each tile type
    tile_count = {}
    for i in range(n):
        tile = tiles[i]
        tile_str = f"{tile[0]} {tile[1]} {tile[2]} {tile[3]}"
        if tile_str in tile_count:
            tile_count[tile_str] += 1
        else:
            tile_count[tile_str] = 1
    
    # Check if we can fill the top-left quadrant
    half_m = m // 2
    for i in range(half_m):
        for j in range(half_m):
            # Find a tile that can fit in the position (i, j)
            found = False
            for tile in tiles:
                if tile[0] == tile[3] and tile[1] == tile[2]:
                    if tile_count[f"{tile[0]} {tile[1]} {tile[2]} {tile[3]}"] > 0:
                        tile_count[f"{tile[0]} {tile[1]} {tile[2]} {tile[3]}"] -= 1
                        found = True
                        break
            if not found:
                return "NO"
    
    return "YES"

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    t = int(data[index])
    index += 1
    results = []
    
    for _ in range(t):
        n = int(data[index])
        m = int(data[index + 1])
        index += 2
        
        tiles = []
        for _ in range(n):
            tile = [
                int(data[index]), int(data[index + 1]),
                int(data[index + 2]), int(data[index + 3])
            ]
            index += 4
            tiles.append(tile)
        
        result = can_construct_symmetric_square(n, m, tiles)
        results.append(result)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()