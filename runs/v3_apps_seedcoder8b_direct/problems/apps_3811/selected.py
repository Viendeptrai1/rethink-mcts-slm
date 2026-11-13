import sys
from math import gcd
from functools import reduce

def find_wcd(n, pairs):
    def gcd_of_list(numbers):
        return reduce(gcd, numbers)

    def lcm(x, y):
        return x * y // gcd(x, y)

    def lcm_of_list(numbers):
        return reduce(lcm, numbers)

    # Extract all numbers from pairs
    all_numbers = [a for a, b in pairs] + [b for a, b in pairs]

    # Calculate the GCD of all numbers
    overall_gcd = gcd_of_list(all_numbers)

    # If the GCD is 1, there is no WCD greater than 1
    if overall_gcd == 1:
        return -1

    # Calculate the LCM of all numbers
    overall_lcm = lcm_of_list(all_numbers)

    # Find the WCD by dividing the LCM by the GCD
    wcd = overall_lcm // overall_gcd

    return wcd

def main():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    pairs = []
    index = 1
    for _ in range(n):
        a = int(data[index])
        b = int(data[index + 1])
        pairs.append((a, b))
        index += 2
    
    result = find_wcd(n, pairs)
    print(result)

if __name__ == "__main__":
    main()