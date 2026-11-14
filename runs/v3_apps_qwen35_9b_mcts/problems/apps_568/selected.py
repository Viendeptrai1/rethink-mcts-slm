import sys

def solve():
    input_data = sys.stdin.read().strip()
    if not input_data:
        return
    n = int(input_data)
    MOD = 10**9 + 7
    
    # Total ways to distribute coins: each of 3n gnomes can have 1, 2, or 3 coins.
    # Total = 3^(3n)
    total_ways = pow(3, 3 * n, MOD)
    
    # Bad ways: Tanya is NOT satisfied.
    # The condition for Tanya being satisfied is: exists i such that a[i] + a[i+n] + a[i+2n] != 6.
    # Tanya is NOT satisfied if for ALL i, a[i] + a[i+n] + a[i+2n] == 6.
    # The triplets (a[i], a[i+n], a[i+2n]) for i=0..n-1 are disjoint and cover all 3n gnomes.
    # We need to count the number of ways to form a triplet (x, y, z) with x,y,z in {1,2,3} such that x+y+z=6.
    # Possible triplets:
    # (1,2,3) -> 6
    # (1,3,2) -> 6
    # (2,1,3) -> 6
    # (2,2,2) -> 6
    # (2,3,1) -> 6
    # (3,1,2) -> 6
    # (3,2,1) -> 6
    # There are exactly 7 such triplets.
    # Since there are n such independent triplets, the number of bad ways is 7^n.
    
    bad_ways = pow(7, n, MOD)
    
    # Result = (Total - Bad) % MOD
    ans = (total_ways - bad_ways) % MOD
    print(ans)

if __name__ == "__main__":
    solve()