import sys

def find_smallest_n(m):
    def count_ways(n):
        count = 0
        for a in range(1, n + 1):
            for b in range(a, n // a + 1):
                for c in range(b, n // (a * b) + 1):
                    d = n // (a * b * c)
                    if a * b * c * d == n and d >= c:
                        count += 1
        return count

    if m == 1:
        return 8

    low, high = 1, 10**15
    result = -1

    while low <= high:
        mid = (low + high) // 2
        if count_ways(mid) == m:
            result = mid
            high = mid - 1
        elif count_ways(mid) < m:
            low = mid + 1
        else:
            high = mid - 1

    return result

if __name__ == "__main__":
    m = int(sys.stdin.read().strip())
    print(find_smallest_n(m))