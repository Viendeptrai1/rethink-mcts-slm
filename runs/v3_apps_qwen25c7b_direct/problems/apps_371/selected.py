def find_min_n(m):
    def count_ways(n, k):
        total_ways = 0
        i = 1
        while i <= n:
            j = i * k
            if j > n:
                break
            k_j = j * k
            if k_j > n:
                total_ways += 1
            else:
                l_kj = k_j * k
                if l_kj > n:
                    total_ways += 1
                else:
                    total_ways += 1
            i += 1
        return total_ways

    left, right = 1, 10**18
    result = -1
    while left <= right:
        mid = (left + right) // 2
        ways = count_ways(mid, 2)
        if ways == m:
            result = mid
            right = mid - 1
        elif ways < m:
            left = mid + 1
        else:
            right = mid - 1
    return result

# Example usage:
m = int(input().strip())
print(find_min_n(m))