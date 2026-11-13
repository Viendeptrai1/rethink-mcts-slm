import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    n = int(input_data[0])
    MOD = 10**9 + 7

    # Total ways to assign 1, 2, or 3 coins to 3n positions
    total = pow(3, 3 * n, MOD)

    # We need to subtract the number of ways where for ALL i in [0, n-1]:
    # a[i] + a[i+n] + a[i+2n] == 6
    #
    # Let x_i = a[i], y_i = a[i+n], z_i = a[i+2n].
    # The condition is x_i + y_i + z_i = 6 for all i.
    # The variables (x_i, y_i, z_i) are independent for each i.
    # For a single triplet (x, y, z) where x,y,z in {1,2,3}, how many solutions satisfy x+y+z=6?
    # Possible sums:
    # 1+1+4 (no), 1+2+3 (yes), 1+3+2 (yes), 2+1+3 (yes), 2+2+2 (yes), 2+3+1 (yes), 3+1+2 (yes), 3+2+1 (yes), 3+3+0 (no)
    # Valid permutations of (1,2,3): 3! = 6
    # Valid permutation of (2,2,2): 1
    # Total valid triplets per group = 7.
    #
    # Since there are n independent groups, the number of "bad" configurations (where Tanya is NOT satisfied) is 7^n.
    #
    # Answer = Total - Bad = 3^(3n) - 7^n

    bad = pow(7, n, MOD)
    ans = (total - bad) % MOD
    print(ans)

if __name__ == "__main__":
    solve()