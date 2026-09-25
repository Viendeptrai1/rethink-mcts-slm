import sys
from collections import Counter
from math import gcd
from functools import reduce

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    divisors = list(map(int, data[1:]))
    
    # Count the occurrences of each divisor
    count = Counter(divisors)
    
    # Find all divisors that appear exactly twice
    potential_gcds = [d for d, c in count.items() if c == 2]
    
    # Find the GCD of these potential GCDs
    actual_gcd = reduce(gcd, potential_gcds)
    
    # Separate the divisors into those belonging to x and those belonging to y
    divisors_x = set()
    divisors_y = set()
    
    for d in divisors:
        if d % actual_gcd == 0:
            divisors_x.add(d)
        else:
            divisors_y.add(d)
    
    # Calculate x and y
    x = reduce(lambda a, b: a * b // gcd(a, b), divisors_x)
    y = reduce(lambda a, b: a * b // gcd(a, b), divisors_y)
    
    print(x, y)

if __name__ == "__main__":
    main()