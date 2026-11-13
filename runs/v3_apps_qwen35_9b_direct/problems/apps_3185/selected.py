import sys
import math

def solve():
    s = sys.stdin.read().strip()
    if not s:
        return
    n = len(s)
    if n == 1:
        val = int(s)
        if val == 1:
            print(1)
        elif val == 2:
            print(2)
        else:
            print(1)
        return

    # Approximate n using Stirling's formula: log10(n!) ~ n*log10(n/e) + 0.5*log10(2*pi*n)
    # We'll use binary search with log10 factorial computed via Kamenetsky's approximation
    # or direct summation of log10 for verification if needed.
    # Given n! has up to 10^6 digits, n is around 10^6 * log10(10^6) ~ 6*10^6? Actually:
    # log10(n!) ~ n log10 n - n log10 e. If log10(n!) = 10^6, then n log10 n ~ 10^6.
    # Solving roughly: if n=10^5, log10 n=5, n log10 n = 5*10^5. If n=2*10^5, log10 n~5.3, product~1.06*10^6.
    # So n is around 200,000 to 300,000 for 10^6 digits. Binary search range [1, 3000000] is safe.

    def log10_factorial_approx(x):
        if x <= 1:
            return 0.0
        # Kamenetsky's formula
        return x * math.log10(x / math.e) + 0.5 * math.log10(2 * math.pi * x)

    low = 1
    high = 3000000  # sufficient upper bound
    ans = 1

    while low <= high:
        mid = (low + high) // 2
        if log10_factorial_approx(mid) >= n - 1e-9:
            ans = mid
            high = mid - 1
        else:
            low = mid + 1

    # Verify the candidate by computing log10 sum precisely to avoid off-by-one due to approximation
    # Compute sum of log10(i) for i=1..ans and check if it's close to n
    # But summing 300k logs is fast enough.
    # However, to be absolutely safe against floating point issues near boundaries, we can do a precise check.
    # We'll compute the exact number of digits for ans and ans-1.
    # Number of digits = floor(log10(n!)) + 1
    # We'll compute log_sum = sum(log10(i) for i in 1..ans)
    # But doing this for every binary search step is too slow. Instead, do it once at the end.

    # Re-calculate precise log sum for the candidate
    log_sum = 0.0
    for i in range(1, ans + 1):
        log_sum += math.log10(i)
    digits = int(math.floor(log_sum)) + 1

    if digits == n:
        print(ans)
    else:
        # Try ans-1
        log_sum_prev = log_sum - math.log10(ans)
        digits_prev = int(math.floor(log_sum_prev)) + 1
        if digits_prev == n:
            print(ans - 1)
        else:
            # Try ans+1 just in case approximation was slightly low
            log_sum_next = log_sum + math.log10(ans + 1)
            digits_next = int(math.floor(log_sum_next)) + 1
            if digits_next == n:
                print(ans + 1)
            else:
                # Fallback: brute force small range around ans
                for cand in range(max(1, ans - 5), ans + 6):
                    log_sum_cand = 0.0
                    for i in range(1, cand + 1):
                        log_sum_cand += math.log10(i)
                    if int(math.floor(log_sum_cand)) + 1 == n:
                        print(cand)
                        return

if __name__ == "__main__":
    solve()