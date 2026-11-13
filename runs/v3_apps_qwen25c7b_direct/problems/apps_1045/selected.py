def max_pyramid_height(n):
    height = 0
    total_cubes = 0
    while total_cubes < n:
        height += 1
        total_cubes += height
    return height if total_cubes == n else height - 1

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    result = max_pyramid_height(n)
    print(result)