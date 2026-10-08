import math
from functools import reduce

def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)

def find_time_for_all_clocks_to_point_upward(N, T):
    return reduce(lcm, T)

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    T = list(map(int, data[1:]))
    
    result = find_time_for_all_clocks_to_point_upward(N, T)
    print(result)