import sys

def max_pyramid_height(n):
    level = 0
    total_cubes = 0
    while total_cubes <= n:
        level += 1
        total_cubes += level
    return level - 1

if __name__ == "__main__":
    n = int(sys.stdin.read().strip())
    print(max_pyramid_height(n))