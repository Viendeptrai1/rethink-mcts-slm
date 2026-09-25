import sys

def can_construct_symmetric_square(tiles, m):
    if m % 2 != 0:
        return "NO"
    
    # Check if there exists a tile that can cover the center 2x2 block
    center_tile_found = False
    for tile in tiles:
        if tile[0][0] == tile[1][1] and tile[0][1] == tile[1][0]:
            center_tile_found = True
            break
    
    if not center_tile_found:
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
                (int(data[index]), int(data[index + 1])),
                (int(data[index + 2]), int(data[index + 3]))
            ]
            tiles.append(tile)
            index += 4
        
        result = can_construct_symmetric_square(tiles, m)
        results.append(result)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()