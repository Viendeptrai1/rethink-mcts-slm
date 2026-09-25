import sys
from collections import Counter
from math import gcd
from functools import reduce

def find_gcd(numbers):
    return reduce(gcd, numbers)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    divisors = list(map(int, data[1:]))
    
    # Count the occurrences of each divisor
    divisor_count = Counter(divisors)
    
    # Find all divisors that appear exactly twice
    potential_gcds = [d for d, count in divisor_count.items() if count == 2]
    
    # Find the GCD of these potential GCDs
    actual_gcd = find_gcd(potential_gcds)
    
    # Separate divisors into those divisible by the GCD and those not
    x_divisors = set(d for d in divisors if d % actual_gcd == 0)
    y_divisors = set(divisors) - x_divisors
    
    # Calculate x and y
    x = reduce(lambda a, b: a * b // gcd(a, b), x_divisors)
    y = reduce(lambda a, b: a * b // gcd(a, b), y_divisors)
    
    print(x, y)

if __name__ == "__main__":
    main()