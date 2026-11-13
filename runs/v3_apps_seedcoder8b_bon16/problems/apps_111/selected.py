def kth_smallest_divisor(n, k):
    divisors = []
    
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            divisors.append(i)
            if i != n // i:
                divisors.append(n // i)
    
    divisors.sort()
    
    if len(divisors) < k:
        return -1
    else:
        return divisors[k - 1]

import sys

def main():
    input = sys.stdin.read
    data = input().strip().split()
    n = int(data[0])
    k = int(data[1])
    
    result = kth_smallest_divisor(n, k)
    print(result)

if __name__ == "__main__":
    main()