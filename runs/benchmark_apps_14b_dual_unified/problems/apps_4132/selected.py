import sys
from math import gcd
from functools import reduce

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    A = list(map(int, data[1:]))
    
    result = reduce(gcd, A)
    print(result)

if __name__ == "__main__":
    main()