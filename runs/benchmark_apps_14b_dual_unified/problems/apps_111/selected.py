import sys
import math

def kth_smallest_divisor(n, k):
    def count_divisors_up_to(x):
        count = 0
        for i in range(1, int(math.sqrt(x)) + 1):
            if x % i == 0:
                count += 1
                if i != x // i:
                    count += 1
        return count

    if k > count_divisors_up_to(n):
        return -1

    low, high = 1, n
    while low < high:
        mid = (low + high) // 2
        if count_divisors_up_to(mid) >= k:
            high = mid
        else:
            low = mid + 1

    return low

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    k = int(data[1])
    result = kth_smallest_divisor(n, k)
    print(result)