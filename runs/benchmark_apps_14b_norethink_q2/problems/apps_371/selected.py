import math

def find_smallest_n(m):
    def count_ways(n):
        count = 0
        for k in range(2, n + 1):
            total = 0
            current = 1
            for _ in range(4):
                total += current
                if total > n:
                    break
                current *= k
            if total <= n:
                count += 1
        return count

    if m == 1:
        return 8

    low, high = 1, 10**15
    result = -1

    while low <= high:
        mid = (low + high) // 2
        if count_ways(mid) >= m:
            result = mid
            high = mid - 1
        else:
            low = mid + 1

    return result

# Read input
m = int(input().strip())

# Find and print the smallest n
print(find_smallest_n(m))