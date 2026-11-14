import sys

def solve():
    try:
        input_data = sys.stdin.read().strip()
        if not input_data:
            return
        n = int(input_data)
    except ValueError:
        return

    # We need to find m and k such that n = m^2 - k^2 = (m-k)(m+k)
    # Let a = m-k and b = m+k, then n = a*b and b >= a.
    # Also, m = (a+b)/2 and k = (b-a)/2.
    # For m and k to be integers, a and b must have the same parity.
    # Since their product n = a*b, if n is odd, both a and b are odd (same parity).
    # If n is even, for a and b to have the same parity, both must be even (since if one is odd and one even, product is even but parities differ).
    # Therefore, a solution exists if:
    # 1. n is odd (and n > 1, because if n=1, a=1, b=1 => m=1, k=0 which is valid, but let's check constraints. n>=1. 1=1^2-0^2 works).
    # 2. n is divisible by 4.
    # If n is even but not divisible by 4 (i.e., n % 4 == 2), no solution exists.

    if n % 2 == 0:
        if n % 4 != 0:
            print("impossible")
            return
        # n is divisible by 4. We can try to find factors.
        # To maximize chances or just find any, we can iterate.
        # Since n <= 10^9, O(sqrt(n)) is fine.
        # We want a and b such that a*b = n, a <= b, and a, b are both even.
        # Let a = 2*x, b = 2*y. Then 4xy = n => xy = n/4.
        # We can find any factorization of n/4. The simplest is x=1, y=n/4.
        # Then a=2, b=2*(n/4) = n/2.
        # Check parity: a=2 (even), b=n/2. Since n is divisible by 4, n/2 is even. So parities match.
        # So for any n divisible by 4, we can use a=2, b=n/2.
        a = 2
        b = n // 2
        m = (a + b) // 2
        k = (b - a) // 2
        print(f"{m} {k}")
    else:
        # n is odd.
        # We can use a=1, b=n. Both are odd, so parities match.
        a = 1
        b = n
        m = (a + b) // 2
        k = (b - a) // 2
        print(f"{m} {k}")

if __name__ == "__main__":
    solve()