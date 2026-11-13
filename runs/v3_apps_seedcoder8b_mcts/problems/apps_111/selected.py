import sys
import math

def kth_smallest_divisor(n, k):
    divisors = []
    for i in range(1, int(math.sqrt(n)) + 1):
        if n % i == 0:
            divisors.append(i)
            if i != n // i:
                divisors.append(n // i)
    divisors.sort()
    if k <= len(divisors):
        return divisors[k - 1]
    else:
        return -1

def main():
    input = sys.stdin.read
    data = input().strip().split()
    n = int(data[0])
    k = int(data[1])
    result = kth_smallest_divisor(n, k)
    print(result)

if __name__ == "__main__":
    main()