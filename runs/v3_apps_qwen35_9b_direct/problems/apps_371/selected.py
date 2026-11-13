import sys

def solve():
    try:
        line = sys.stdin.read().strip()
        if not line:
            return
        m = int(line)
    except ValueError:
        return

    # Precompute f(n) for n from 1 upwards until f(n) >= m
    # We stop when f(n) > m and the next value won't reach m, or we find m.
    # Since f(n) is non-decreasing, we can binary search or linear scan.
    # Given m up to 1e15, linear scan up to ~1e6 is too slow? Let's estimate.
    # f(n) grows roughly as n^2 / (2 * log^2 n) or similar? Actually, let's derive bounds.
    # The number of ways is the number of integers k >= 2 such that there exists a starting value a >= 1
    # with a * (1 + k + k^2 + k^3) <= n.
    # For a fixed k, the max a is floor(n / S_k) where S_k = 1+k+k^2+k^3.
    # So count_k = floor(n / S_k).
    # Total ways f(n) = sum_{k>=2} floor(n / S_k).
    # We need to find smallest n such that f(n) == m.
    # Since f(n) is monotonic, we can binary search for n.
    # What is the upper bound for n?
    # If k=2, S_2 = 1+2+4+8 = 15. Then count_2 = floor(n/15).
    # If m = 1e15, then n/15 approx 1e15 => n approx 1.5e16.
    # So n can be up to ~1.5e16. Binary search is feasible.
    # Lower bound: n=1.
    # Upper bound: Let's set high = 2 * 10**16 (safe for m=1e15).
    # Actually, if m=1, n=8. If m=1e15, n ~ 1.5e16.
    # We'll use binary search.

    def count_ways(n):
        if n < 1:
            return 0
        total = 0
        k = 2
        while True:
            # S_k = 1 + k + k^2 + k^3
            # We can compute iteratively to avoid large powers if k is huge, but k won't be huge because S_k grows fast.
            # For n up to 1e16, k won't exceed ~1e4 because 1+k+k^2+k^3 > n when k is large.
            # Actually, if k=10000, k^3 = 1e12, which is fine. If k=1e5, k^3=1e15. If k=2e5, k^3=8e15.
            # So k goes up to maybe 2e5. Loop is fine.
            s_k = 1 + k + k*k + k*k*k
            if s_k > n:
                break
            total += n // s_k
            k += 1
            # Safety break to prevent infinite loop in case of logic error
            if k > 2000000:
                break
        return total

    low = 1
    high = 2 * 10**16  # Sufficiently large for m=1e15
    ans = -1

    while low <= high:
        mid = (low + high) // 2
        val = count_ways(mid)
        if val == m:
            ans = mid
            # Try to find a smaller n
            high = mid - 1
        elif val < m:
            low = mid + 1
        else:
            high = mid - 1

    if ans != -1:
        print(ans)
    else:
        print(-1)

if __name__ == "__main__":
    solve()