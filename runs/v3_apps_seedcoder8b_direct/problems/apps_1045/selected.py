def max_pyramid_height(n):
    height = 0
    cubes_used = 0
    while cubes_used + (height + 1) <= n:
        height += 1
        cubes_used += height
    return height

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    n = int(input().strip())
    print(max_pyramid_height(n))