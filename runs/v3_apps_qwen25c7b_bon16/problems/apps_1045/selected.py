def max_pyramid_height(cubes):
    height = 0
    current_level_cubes = 0
    
    while cubes >= 0:
        height += 1
        current_level_cubes += height
        if current_level_cubes > cubes:
            return height - 1
        cubes -= current_level_cubes
    
    return height

# Example usage:
n = int(input().strip())
print(max_pyramid_height(n))