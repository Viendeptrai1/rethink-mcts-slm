import sys
import math

def find_swimming_pool_dimensions(n):
    # Start from m = ceil(sqrt(n)) and go up
    for m in range(math.ceil(math.sqrt(n)), int(2 * math.sqrt(n)) + 1):
        k_squared = m * m - n
        if k_squared >= 0:
            k = int(math.sqrt(k_squared))
            if k * k == k_squared:
                return m, k
    return "impossible"

if __name__ == "__main__":
    n = int(sys.stdin.read().strip())
    result = find_swimming_pool_dimensions(n)
    if result == "impossible":
        print("impossible")
    else:
        m, k = result
        print(m, k)