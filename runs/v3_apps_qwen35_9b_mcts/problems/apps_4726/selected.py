import sys
import math

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    m = int(input_data[0])
    n = int(input_data[1])
    t = int(input_data[2])
    
    operations = 0
    
    if t == 1:
        # O(n!)
        # Check if n! <= m
        # Since n can be up to 10^9, we cannot compute factorial directly.
        # However, n! grows very fast. 20! is already ~2.4e18 which is > 10^9.
        # So if n >= 20, it's definitely TLE (since m <= 10^9).
        if n >= 20:
            print("TLE")
            return
        operations = math.factorial(n)
    elif t == 2:
        # O(2^n)
        # Check if 2^n <= m
        # 2^30 is ~1e9. So if n >= 30, it's likely TLE.
        # We can check using bit_length or log2, but direct comparison with care is safer.
        # Since m <= 10^9, and 2^29 = 536870912, 2^30 = 1073741824.
        # If n >= 30, 2^n > 10^9 >= m.
        if n >= 30:
            print("TLE")
            return
        operations = 1 << n
    elif t == 3:
        # O(n^4)
        # Check if n^4 <= m
        # If n is large, n^4 will overflow standard integers or exceed m quickly.
        # n^4 <= m => n <= m^(1/4). Since m <= 10^9, m^(1/4) <= 10^(9/4) = 10^2.25 approx 177.
        # So if n > 200, it's definitely TLE.
        if n > 200:
            print("TLE")
            return
        operations = n ** 4
    elif t == 4:
        # O(n^3)
        # n^3 <= m => n <= m^(1/3). m <= 10^9 => n <= 1000.
        # If n > 2000, definitely TLE.
        if n > 2000:
            print("TLE")
            return
        operations = n ** 3
    elif t == 5:
        # O(n^2)
        # n^2 <= m => n <= sqrt(m). m <= 10^9 => n <= 31622.
        # If n > 100000, definitely TLE.
        if n > 100000:
            print("TLE")
            return
        operations = n ** 2
    elif t == 6:
        # O(n log n)
        # n * log2(n) <= m
        # If n is very large, this exceeds m.
        # n * log2(n) <= 10^9. If n = 10^9, log2(n) ~ 30, product ~ 3e10 > 10^9.
        # We can estimate: if n > 2*10^8, then n*log2(n) > 2e8 * 28 > 5.6e9 > 10^9.
        # So if n > 300,000,000, definitely TLE.
        if n > 300000000:
            print("TLE")
            return
        # Compute n * log2(n)
        # Use math.log2
        operations = int(n * math.log2(n))
    elif t == 7:
        # O(n)
        # n <= m
        if n > m:
            print("TLE")
            return
        operations = n
    
    if operations <= m:
        print("AC")
    else:
        print("TLE")

if __name__ == "__main__":
    solve()