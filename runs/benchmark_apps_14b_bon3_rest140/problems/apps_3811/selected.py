import sys
from math import gcd

def find_wcd(pairs):
    # Calculate the GCD of all numbers in the pairs
    overall_gcd = pairs[0][0]
    for a, b in pairs:
        overall_gcd = gcd(overall_gcd, a)
        overall_gcd = gcd(overall_gcd, b)
    
    # If the overall GCD is 1, then no WCD exists
    if overall_gcd == 1:
        return -1
    
    # Otherwise, any divisor of the overall GCD greater than 1 is a valid WCD
    return overall_gcd

def main():
    import sys
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
    
    result = find_wcd(pairs)
    print(result)

if __name__ == "__main__":
    main()