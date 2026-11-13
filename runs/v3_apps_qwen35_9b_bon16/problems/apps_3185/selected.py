import sys
import math

def solve():
    line = sys.stdin.read().strip()
    if not line:
        return
    try:
        n_fact = int(line)
    except ValueError:
        return
    if n_fact == 1:
        print(1)
        return
    # Binary search for n such that n! == n_fact
    low = 1
    high = 10**6  # sufficient since 10^6 digits implies n around 5e5
    while low <= high:
        mid = (low + high) // 2
        fact_mid = math.factorial(mid)
        if fact_mid == n_fact:
            print(mid)
            return
        elif fact_mid < n_fact:
            low = mid + 1
        else:
            high = mid - 1

if __name__ == "__main__":
    solve()