import math

def max_pyramid_height(n):
    # Using the quadratic formula to solve k(k+1)/2 <= n for k
    k = int((-1 + math.sqrt(1 + 8 * n)) / 2)
    return k

# Example usage:
if __name__ == "__main__":
    n = int(input())
    print(max_pyramid_height(n))