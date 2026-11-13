def find_minimum_n(m):
    def count_ways(n, k):
        ways = 0
        for a in range(1, n + 1):
            b = a * k
            c = b * k
            d = c * k
            if d <= n:
                ways += 1
            else:
                break
        return ways

    if m == 1:
        return 8

    for n in range(1, 10**6):
        k = 2
        while k <= n:
            if count_ways(n, k) == m:
                return n
            k += 1

    return -1

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    m = int(input().strip())
    print(find_minimum_n(m))