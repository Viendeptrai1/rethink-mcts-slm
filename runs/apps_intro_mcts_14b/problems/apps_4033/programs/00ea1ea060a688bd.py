import sys
import math

def min_perimeter(a, b):
    def factors(n):
        result = set()
        for i in range(1, int(math.sqrt(n)) + 1):
            if n % i == 0:
                result.add(i)
                result.add(n // i)
        return result
    
    red_factors = factors(a)
    blue_factors = factors(b)
    
    min_peri = float('inf')
    
    for r in red_factors:
        for c in blue_factors:
            if r * c == a + b:
                # Check if either red or blue forms a rectangle
                if (a % r == 0 and b % (c - r) == 0) or (b % c == 0 and a % (r - c) == 0):
                    peri = 2 * (r + c)
                    min_peri = min(min_peri, peri)
    
    return min_peri

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    a = int(data[0])
    b = int(data[1])
    print(min_perimeter(a, b))

if __name__ == "__main__":
    main()