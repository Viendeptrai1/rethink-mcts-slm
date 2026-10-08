import sys
from math import gcd
from functools import reduce

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    A = list(map(int, data[1:]))
    
    # Calculate the GCD of the entire list
    current_gcd = reduce(gcd, A)
    
    # If the current GCD is already the maximum possible, return it
    if current_gcd == 1:
        print(1)
        return
    
    # Check if we can increase the GCD by replacing any element
    max_possible_gcd = 1
    for i in range(N):
        # Calculate the GCD of the list excluding the i-th element
        gcd_excluding_i = reduce(gcd, A[:i] + A[i+1:])
        
        # Find the GCD of gcd_excluding_i and all other elements
        for j in range(N):
            if j != i:
                max_possible_gcd = max(max_possible_gcd, gcd(gcd_excluding_i, A[j]))
    
    print(max_possible_gcd)

if __name__ == "__main__":
    main()