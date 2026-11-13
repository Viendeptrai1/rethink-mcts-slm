def minimum_final_health(N, A):
    from math import gcd
    from functools import reduce

    # Calculate the GCD of all the health values
    overall_gcd = reduce(gcd, A)
    
    # The minimum possible final health of the last monster alive
    return overall_gcd

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    A = list(map(int, data[1:]))
    
    result = minimum_final_health(N, A)
    print(result)