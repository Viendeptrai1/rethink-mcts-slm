import sys

def can_construct_symmetric_square(tiles, m):
    # Check if we can fill the top-left quadrant of the square
    def can_fill_quadrant(quad_size):
        if quad_size == 0:
            return True
        for i in range(quad_size):
            for j in range(quad_size):
                found = False
                for tile in tiles:
                    if (tile[0][0] == tile[1][1] and tile[0][1] == tile[1][0] and
                        tile[0][0] == tile[0][1] and tile[0][0] == tile[1][1]):
                        found = True
                        break
                if not found:
                    return False
        return True

    # Check if we can fill the entire square
    if m % 2 == 0:
        return can_fill_quadrant(m // 2)
    else:
        return can_fill_quadrant((m // 2) + 1)

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
        
        if can_construct_symmetric_square(tiles, m):
            results.append("YES")
        else:
            results.append("NO")
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()