import sys
from collections import Counter
from math import gcd

def find_x_y(n, divisors):
    # Count the frequency of each divisor
    freq = Counter(divisors)
    
    # Find the GCD candidates (divisors that appear exactly twice)
    gcd_candidates = [d for d, count in freq.items() if count == 2]
    
    # Sort the GCD candidates in descending order
    gcd_candidates.sort(reverse=True)
    
    # Try the largest GCD candidate first
    for g in gcd_candidates:
        # Remove the GCD from the frequency counter
        del freq[g]
        
        # Calculate the remaining divisors for x and y
        x_divs = set()
        y_divs = set()
        for d, count in freq.items():
            if count == 1:
                if d % g == 0:
                    x_divs.add(d // g)
                    y_divs.add(d // g)
                else:
                    x_divs.add(d)
                    y_divs.add(d)
        
        # Calculate x and y
        x = 1
        y = 1
        for d in x_divs:
            x *= d
        for d in y_divs:
            y *= d
        
        # Check if the product of x and y matches the product of the original divisors
        if x * y == g * g * (n // 2):
            return x, y
    
    return None, None

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    divisors = list(map(int, data[1:]))
    
    x, y = find_x_y(n, divisors)
    print(x, y)

if __name__ == "__main__":
    main()