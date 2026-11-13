import sys

def solve():
    try:
        input_data = sys.stdin.read().strip()
        if not input_data:
            return
        m = int(input_data)
    except ValueError:
        return

    # If m is 1, answer is 8 as per example
    if m == 1:
        print(8)
        return

    # We need to find the smallest n such that count_ways(n) == m.
    # count_ways(n) is the number of integer sequences (a, b, c, d) such that:
    # 1 <= a
    # b = k*a, c = k*b, d = k*c with k > 1 integer
    # d <= n  =>  a * k^3 <= n  =>  a <= n / k^3
    # Since a >= 1, for a fixed k, the number of choices for a is floor(n / k^3).
    # So count_ways(n) = sum_{k=2, k^3 <= n} floor(n / k^3)
    
    # Let f(n) = sum_{k=2}^{floor(n^(1/3))} floor(n / k^3)
    # f(n) is non-decreasing with n.
    # We can binary search for the smallest n such that f(n) >= m.
    # Then check if f(n) == m.

    def count_ways(n):
        total = 0
        k = 2
        while True:
            k3 = k * k * k
            if k3 > n:
                break
            total += n // k3
            k += 1
        return total

    # Estimate upper bound for binary search.
    # For large n, count_ways(n) approx n * sum_{k>=2} 1/k^3 = n * (zeta(3) - 1)
    # zeta(3) approx 1.202, so sum approx 0.202.
    # So n approx m / 0.202 approx 5 * m.
    # Given m up to 10^15, n can be around 5e15. Let's set high = 6e15 + 100.
    # To be safe, we can double high until count_ways(high) >= m.

    low = 1
    high = 10**7
    while count_ways(high) < m:
        high *= 2
        if high > 10**18:
            # If we exceed reasonable bounds and still not found, then impossible
            break

    if high > 10**18 or count_ways(high) < m:
        print("-1")
        return

    ans = -1
    while low <= high:
        mid = (low + high) // 2
        c = count_ways(mid)
        if c == m:
            ans = mid
            # Try to find smaller
            high = mid - 1
        elif c < m:
            low = mid + 1
        else:
            high = mid - 1

    if ans != -1:
        print(ans)
    else:
        print("-1")

if __name__ == "__main__":
    solve()