import sys
import math

def gcd(x, y):
    while y:
        x, y = y, x % y
    return x

def lcm(x, y):
    return x * y // gcd(x, y)

def min_perimeter(a, b):
    total_tiles = a + b
    # Find the smallest rectangle that can contain a + b tiles
    min_side = int(math.sqrt(total_tiles))
    while total_tiles % min_side != 0:
        min_side -= 1
    max_side = total_tiles // min_side
    
    # Check if we can form the required rectangles
    for i in range(1, int(math.sqrt(a)) + 1):
        if a % i == 0:
            j = a // i
            if (i <= min_side and j <= max_side) or (j <= min_side and i <= max_side):
                for k in range(1, int(math.sqrt(b)) + 1):
                    if b % k == 0:
                        l = b // k
                        if (k <= min_side and l <= max_side) or (l <= min_side and k <= max_side):
                            return 2 * (min_side + max_side)
    
    return -1  # This line should never be reached due to problem constraints

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    a = int(data[0])
    b = int(data[1])
    result = min_perimeter(a, b)
    print(result)