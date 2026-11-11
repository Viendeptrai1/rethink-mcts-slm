import sys

def max_pyramid_height(n):
    height = 0
    while n > 0:
        height += 1
        n -= height * (height + 1) // 2
    if n < 0:
        height -= 1
    return height

if __name__ == "__main__":
    n = int(sys.stdin.read())
    print(max_pyramid_height(n))