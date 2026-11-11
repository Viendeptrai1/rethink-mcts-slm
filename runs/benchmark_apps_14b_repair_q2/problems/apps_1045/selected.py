import sys

def max_pyramid_height(n):
    height = 0
    current_level_cubes = 0
    while n > 0:
        height += 1
        current_level_cubes += height
        if current_level_cubes > n:
            return height - 1
    return height

if __name__ == "__main__":
    n = int(sys.stdin.read())
    print(max_pyramid_height(n))