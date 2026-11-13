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
    # Let a = m-k and b = m+k, then n = a * b
    # Also, m = (a+b)/2 and k = (b-a)/2
    # For m and k to be integers:
    # 1. a and b must have the same parity (both even or both odd) -> their product n must be odd or a multiple of 4
    # 2. b >= a (since k >= 0)
    # 3. a * b = n
    # Since b = n/a, we iterate a from 1 up to sqrt(n)
    
    if n % 2 == 0 and n % 4 != 0:
        # If n is even but not divisible by 4, it cannot be written as difference of two squares
        print("impossible")
        return

    limit = int(n**0.5)
    for a in range(1, limit + 1):
        if n % a == 0:
            b = n // a
            # Check parity: a and b must have same parity
            if (a % 2) == (b % 2):
                # Ensure b >= a to keep k non-negative
                if b >= a:
                    m = (a + b) // 2
                    k = (b - a) // 2
                    print(f"{m} {k}")
                    return

    print("impossible")

if __name__ == "__main__":
    solve()