import sys

def max_pyramid_height(n):
    height = 0
    current_level_cubes = 0
    while n >= current_level_cubes:
        height += 1
        current_level_cubes += height
    return height

if __name__ == "__main__":
    n = int(sys.stdin.read())
    print(max_pyramid_height(n))