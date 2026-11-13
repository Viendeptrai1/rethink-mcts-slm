import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    MOD = 10**9 + 7
    
    # Total number of ways to assign 1-3 coins to 3n positions
    # Each position has 3 choices.
    total_ways = pow(3, 3 * n, MOD)
    
    # Calculate the number of ways where Tanya is NOT satisfied.
    # Tanya is NOT satisfied if for ALL i in [0, n-1], the condition holds:
    # a[i] + a[i+n] + a[i+2n] == 6
    # Since each a[k] is in {1, 2, 3}, the only way the sum is 6 is if all three are 2.
    # (1+2+3=6 but order matters? No, the condition is specifically a[i] + a[i+n] + a[i+2n] == 6.
    # Let's re-read carefully: "a_i + a_i + n + a_i + 2n != 6". 
    # The indices are i, i+n, i+2n.
    # If the sum is 6, since min value is 1 and max is 3, the only integer solution for x+y+z=6 with 1<=x,y,z<=3 is x=2, y=2, z=2.
    # Proof: If any is 1, max sum is 1+3+3=7. But we need 6.
    # If x=1, y+z=5. Pairs (2,3), (3,2).
    # If x=3, y+z=3. Pairs (1,2), (2,1).
    # Wait, the problem statement says: "If there is an integer i ... such that sum != 6, then Tanya is satisfied."
    # This means Tanya is satisfied if AT LEAST ONE triplet sums to something other than 6.
    # Conversely, Tanya is NOT satisfied if FOR ALL triplets i in [0, n-1], the sum IS 6.
    # Does sum=6 imply a[i]=2, a[i+n]=2, a[i+2n]=2?
    # Let's check combinations of {1,2,3} that sum to 6:
    # 1+2+3 = 6
    # 2+2+2 = 6
    # 3+1+2 = 6 (same set)
    # So the triplet (a[i], a[i+n], a[i+2n]) must be a permutation of (1,2,3) OR (2,2,2).
    # Wait, the indices in the circle are i, i+n, i+2n. These are distinct positions modulo 3n for n >= 1.
    # Specifically, the set of indices for a fixed i is {i, i+n, i+2n}.
    # As i goes from 0 to n-1, these sets partition the 3n positions into n disjoint triplets.
    # Why disjoint? 
    # Suppose x is in {i, i+n, i+2n} and y is in {j, j+n, j+2n} with i != j (mod n).
    # If x = y, then x = i + k*n and x = j + m*n for k,m in {0,1,2}.
    # So i + k*n = j + m*n => i - j = (m-k)*n.
    # Since 0 <= i, j < n, |i-j| < n. The only multiple of n in this range is 0.
    # So i=j and m=k. Thus the sets are disjoint.
    # Therefore, the condition "For ALL i in [0, n-1], sum == 6" means that for each of the n disjoint triplets, the sum of the three values is 6.
    # For a single triplet (x, y, z) where x,y,z in {1,2,3}, how many solutions to x+y+z=6?
    # Possible multisets:
    # 1) {2, 2, 2} -> Permutations: (2,2,2) -> 1 way.
    # 2) {1, 2, 3} -> Permutations: (1,2,3), (1,3,2), (2,1,3), (2,3,1), (3,1,2), (3,2,1) -> 6 ways.
    # Total ways per triplet = 1 + 6 = 7.
    # Since there are n independent triplets, the number of ways where Tanya is NOT satisfied is 7^n.
    
    bad_ways = pow(7, n, MOD)
    
    # The answer is Total - Bad
    ans = (total_ways - bad_ways) % MOD
    
    print(ans)

if __name__ == '__main__':
    solve()