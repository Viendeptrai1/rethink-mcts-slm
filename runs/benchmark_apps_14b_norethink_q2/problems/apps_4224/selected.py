import sys
from collections import Counter

def max_operations(N, a):
    max_ops = 0
    for num in a:
        # Count the number of 2s and 3s in the prime factorization
        count_2 = 0
        count_3 = 0
        while num % 2 == 0:
            num //= 2
            count_2 += 1
        while num % 3 == 0:
            num //= 3
            count_3 += 1
        # The number of operations is limited by the minimum of count_2 and count_3
        max_ops += min(count_2, count_3)
    return max_ops

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    N = int(data[0])
    a = list(map(int, data[1:]))
    print(max_operations(N, a))

if __name__ == "__main__":
    main()