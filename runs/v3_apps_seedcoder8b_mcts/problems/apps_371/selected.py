def find_minimum_n(m):
    def ways_for_n(n):
        total_ways = 0
        for k in range(2, n + 1):
            a1 = 1
            an = a1 * (k ** 3)
            if an > n:
                break
            sum_geometric = (a1 * (1 - k ** 4)) // (1 - k)
            if sum_geometric <= n:
                total_ways += sum_geometric
        return total_ways

    left, right = 1, 10**15
    result = -1

    while left <= right:
        mid = (left + right) // 2
        if ways_for_n(mid) == m:
            result = mid
            right = mid - 1
        elif ways_for_n(mid) < m:
            left = mid + 1
        else:
            right = mid - 1

    return result

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    m = int(input().strip())
    print(find_minimum_n(m))