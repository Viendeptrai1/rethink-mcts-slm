import sys

def max_pyramid_height(n):
    height = 0
    while n >= height + 1:
        height += 1
        n -= height
    return height

if __name__ == "__main__":
    n = int(sys.stdin.readline().strip())
    print(max_pyramid_height(n))