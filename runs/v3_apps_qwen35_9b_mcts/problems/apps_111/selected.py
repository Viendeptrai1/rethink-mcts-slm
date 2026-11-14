import sys
import math

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    n = int(input_data[0])
    k = int(input_data[1])

    small_divisors = []
    large_divisors = []
    limit = int(math.isqrt(n))

    for i in range(1, limit + 1):
        if n % i == 0:
            small_divisors.append(i)
            if i * i != n:
                large_divisors.append(n // i)

    # small_divisors are in ascending order
    # large_divisors are in descending order (since we iterate i from 1 upwards)
    # We need the k-th smallest divisor overall.
    # The total number of divisors is len(small_divisors) + len(large_divisors).
    # If k <= len(small_divisors), the answer is small_divisors[k-1].
    # If k > len(small_divisors), we need to look into large_divisors.
    # The divisors in large_divisors are the largest ones, in descending order.
    # The (len(small) + 1)-th smallest is the last element of large_divisors.
    # The (len(small) + 2)-th smallest is the second to last, etc.
    # So if k > len(small), the index in large_divisors (0-based) from the end is:
    # index_from_end = k - len(small_divisors)
    # Since large_divisors is descending, the element at position (len(large) - index_from_end) is the answer.
    
    num_small = len(small_divisors)
    num_large = len(large_divisors)
    total = num_small + num_large

    if k > total:
        print(-1)
    elif k <= num_small:
        print(small_divisors[k - 1])
    else:
        # k is in the large part
        # We need the (k - num_small)-th element from the end of large_divisors
        # large_divisors is [n//1, n//2, ...] (descending)
        # The 1st from end is the smallest large divisor (which is the (num_small+1)-th overall)
        # The m-th from end is the m-th smallest among the large divisors
        m = k - num_small
        # Index in large_divisors list: len - m
        idx = num_large - m
        print(large_divisors[idx])

if __name__ == "__main__":
    solve()