import sys
from fractions import Fraction

def main():
    import sys
    import math
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        return abs(a*b) // gcd(a, b)
    
    def solve(n, p, q, projects):
        # Convert all values to fractions to maintain precision
        p = Fraction(p)
        q = Fraction(q)
        projects = [(Fraction(a), Fraction(b)) for a, b in projects]
        
        # Find the maximum ratio of experience to money among all projects
        max_ratio = max(a / b for a, b in projects)
        
        # If the maximum ratio is less than the required ratio, it's impossible to meet both goals
        if max_ratio < p / q:
            print(-1)
            return
        
        # Initialize variables for binary search
        low = Fraction(0)
        high = Fraction(max(p, q))
        
        # Perform binary search with high precision
        epsilon = Fraction(1, 10**12)
        while high - low > epsilon:
            mid = (low + high) / 2
            exp = sum(max(0, mid * a - p) for a, _ in projects)
            money = sum(max(0, mid * b - q) for _, b in projects)
            
            if exp == 0 and money == 0:
                high = mid
            else:
                low = mid
        
        # Print the result with high precision
        print(float(low))
    
    # Read input
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    p = int(data[1])
    q = int(data[2])
    projects = []
    
    index = 3
    for _ in range(n):
        a = int(data[index])
        b = int(data[index + 1])
        projects.append((a, b))
        index += 2
    
    # Solve the problem
    solve(n, p, q, projects)

if __name__ == "__main__":
    main()