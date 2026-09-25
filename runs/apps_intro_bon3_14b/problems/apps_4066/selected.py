import sys
from math import gcd

def lcm(x, y):
    return x * y // gcd(x, y)

def find_min_lcm_pair(n, a):
    min_lcm = float('inf')
    min_pair = (1, 2)
    
    for i in range(n):
        for j in range(i + 1, n):
            current_lcm = lcm(a[i], a[j])
            if current_lcm < min_lcm:
                min_lcm = current_lcm
                min_pair = (i + 1, j + 1)
    
    return min_pair

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:]))
    
    result = find_min_lcm_pair(n, a)
    print(result[0], result[1])

if __name__ == "__main__":
    main()