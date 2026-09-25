import sys
from math import gcd
from functools import reduce

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:]))
    
    # Calculate the GCD of the entire array
    common_gcd = reduce(gcd, a)
    
    # Function to count the number of divisors of a number
    def count_divisors(x):
        count = 0
        for i in range(1, int(x**0.5) + 1):
            if x % i == 0:
                count += 1
                if i != x // i:
                    count += 1
        return count
    
    # Output the number of divisors of the GCD
    print(count_divisors(common_gcd))

if __name__ == "__main__":
    main()