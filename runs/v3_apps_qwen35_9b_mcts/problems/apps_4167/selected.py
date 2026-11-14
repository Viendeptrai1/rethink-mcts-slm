import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    N = int(input_data[0])
    K = int(input_data[1])

    # Count numbers in [1, N] with remainder r modulo K
    # For a given remainder r (0 <= r < K), the count is:
    # (N - r + K) // K if r != 0 else (N + K) // K? 
    # Actually simpler: numbers x in [1, N] such that x % K == r.
    # If r == 0, we want multiples of K: floor(N / K)
    # If r != 0, we want numbers congruent to r mod K: floor((N - r) / K) + 1 if N >= r else 0
    
    def count_with_remainder(r):
        if r == 0:
            return N // K
        else:
            if N < r:
                return 0
            return (N - r) // K + 1

    total = 0
    
    # Case 1: All three numbers have remainder 0 mod K
    c0 = count_with_remainder(0)
    total += c0 * c0 * c0
    
    # Case 2: K is even, and all three numbers have remainder K/2 mod K
    if K % 2 == 0:
        r_half = K // 2
        c_half = count_with_remainder(r_half)
        total += c_half * c_half * c_half
    
    print(total)

if __name__ == "__main__":
    solve()