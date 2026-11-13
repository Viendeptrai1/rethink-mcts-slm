def max_pyramid_height(n):
    height = 0
    current_level_cubes = 0
    level = 1
    
    while n >= current_level_cubes + level:
        current_level_cubes += level
        n -= current_level_cubes
        height += 1
        level += 1
    
    return height

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    n = int(input().strip())
    print(max_pyramid_height(n))