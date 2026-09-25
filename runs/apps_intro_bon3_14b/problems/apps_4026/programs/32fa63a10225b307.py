import sys

def can_construct_symmetric_square(n, m, tiles):
    # Check if the size of the square is odd
    if m % 2 == 1:
        return "NO"
    
    # Create a dictionary to store the frequency of each tile type
    tile_count = {}
    for i in range(n):
        tile = (tiles[2*i], tiles[2*i+1], tiles[2*i+2], tiles[2*i+3])
        if tile in tile_count:
            tile_count[tile] += 1
        else:
            tile_count[tile] = 1
    
    # Check if we can fill the top-left quadrant
    half_m = m // 2
    for i in range(half_m):
        for j in range(half_m):
            # Find a tile that can fit in position (i, j)
            found = False
            for tile, count in tile_count.items():
                if count > 0 and tile[0] == tiles[2*i] and tile[1] == tiles[2*j]:
                    # Check if the corresponding positions in the symmetric part can be filled
                    if tile[2] == tiles[2*(half_m - 1 - j)] and tile[3] == tiles[2*(half_m - 1 - i)]:
                        found = True
                        tile_count[tile] -= 1
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
        for _ in range(2 * n):
            tiles.append(int(data[index]))
            index += 1
        
        result = can_construct_symmetric_square(n, m, tiles)
        results.append(result)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()