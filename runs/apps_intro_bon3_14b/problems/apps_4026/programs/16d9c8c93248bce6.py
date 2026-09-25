import sys

def can_construct_symmetric_square(n, m, tiles):
    # Check if m is odd, if so, it's impossible to construct a symmetric square
    if m % 2 == 1:
        return "NO"
    
    # Create a dictionary to store the count of each unique tile configuration
    tile_count = {}
    for i in range(n):
        top_left, top_right = tiles[2 * i]
        bottom_left, bottom_right = tiles[2 * i + 1]
        # Create a unique key for each tile configuration
        key = (top_left, top_right, bottom_left, bottom_right)
        if key not in tile_count:
            tile_count[key] = 0
        tile_count[key] += 1
    
    # Calculate the number of 2x2 blocks needed
    num_blocks = (m // 2) ** 2
    
    # Check if we have enough tiles to fill the square
    total_tiles = sum(tile_count.values())
    if total_tiles < num_blocks:
        return "NO"
    
    # Check if we can form a symmetric square
    # We need to ensure that for each tile configuration, we have enough to fill the required positions
    for key in tile_count:
        top_left, top_right, bottom_left, bottom_right = key
        # Check if the tile can be used to form a symmetric block
        if top_left != bottom_right or top_right != bottom_left:
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
            tiles.append((int(data[index]), int(data[index + 1])))
            index += 2
        
        result = can_construct_symmetric_square(n, m, tiles)
        results.append(result)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()