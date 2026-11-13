import math
from functools import reduce

def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)

def find_lcm_of_list(numbers):
    return reduce(lcm, numbers)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    T_values = list(map(int, data[1:N+1]))
    
    result = find_lcm_of_list(T_values)
    print(result)

if __name__ == "__main__":
    main()