import sys

# Increase recursion depth just in case, though we use iterative DP
sys.setrecursionlimit(10**6)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        n = int(next(iterator))
    except StopIteration:
        return

    a = []
    b = []
    for _ in range(n):
        a.append(int(next(iterator)))
        b.append(int(next(iterator)))

    MOD = 998244353

    # Count duplicates for combinations formula
    # We need counts of identical pairs (a, b)
    # And counts of identical a's, and identical b's
    
    # Map (a, b) -> count
    pair_counts = {}
    a_counts = {}
    b_counts = {}
    
    for i in range(n):
        pair = (a[i], b[i])
        pair_counts[pair] = pair_counts.get(pair, 0) + 1
        
        val_a = a[i]
        a_counts[val_a] = a_counts.get(val_a, 0) + 1
        
        val_b = b[i]
        b_counts[val_b] = b_counts.get(val_b, 0) + 1

    # Precompute factorials and inverse factorials for combinations
    fact = [1] * (n + 1)
    inv_fact = [1] * (n + 1)
    
    for i in range(2, n + 1):
        fact[i] = (fact[i-1] * i) % MOD
        
    inv_fact[n] = pow(fact[n], MOD - 2, MOD)
    for i in range(n - 1, 1, -1):
        inv_fact[i] = (inv_fact[i+1] * (i + 1)) % MOD

    def nCr(n_val, r_val):
        if r_val < 0 or r_val > n_val:
            return 0
        num = fact[n_val]
        den = (inv_fact[r_val] * inv_fact[n_val - r_val]) % MOD
        return (num * den) % MOD

    # Total permutations = n!
    total_perms = fact[n]

    # Count permutations where A is sorted non-descendingly
    # If there are duplicates in A, the number of distinct permutations that result in 
    # a non-decreasing sequence of A is simply 1 unique arrangement of values, 
    # but since original items are distinct by index, we are counting index permutations.
    # Actually, the condition is on the values. 
    # The number of permutations of indices such that the resulting sequence of A values is sorted non-descendingly
    # is equal to the product of factorials of counts of each distinct value in A.
    # Why? Because for a specific sorted sequence of values, any permutation of indices that maps to those values 
    # while preserving the order of values is valid. Wait, no.
    # Let's re-evaluate.
    # We want the number of permutations p such that A[p_1], A[p_2], ... A[p_n] is non-decreasing.
    # This means the values must appear in sorted order. 
    # If we have k identical values, they can be arranged among themselves in k! ways in the original set of indices,
    # but in the target sorted sequence, their relative order doesn't matter for the "sorted" property, 
    # HOWEVER, we are counting permutations of the original indices.
    # Suppose we have values: 1, 1, 2. Indices: 0, 1, 2.
    # Sorted values: 1, 1, 2.
    # Permutations of indices that yield [1, 1, 2]:
    # [0, 1, 2] -> A[0]=1, A[1]=1, A[2]=2. OK.
    # [1, 0, 2] -> A[1]=1, A[0]=1, A[2]=2. OK.
    # [0, 2, 1] -> 1, 2, 1. No.
    # So for each group of identical values, if there are c identical values, there are c! ways to assign the indices 
    # to the positions occupied by that value, provided the positions are fixed to be the sorted slots.
    # Since the positions for each value are fixed by the sorted order of values, the number of such permutations is 
    # the product of (count of value!) for all distinct values in A.
    
    count_A_sorted = 1
    for count in a_counts.values():
        count_A_sorted = (count_A_sorted * fact[count]) % MOD

    count_B_sorted = 1
    for count in b_counts.values():
        count_B_sorted = (count_B_sorted * fact[count]) % MOD

    # Count permutations where BOTH A and B are sorted non-descendingly.
    # This happens if the sequence of pairs (A, B) is sorted by A AND sorted by B.
    # This implies the sequence of pairs must be non-decreasing in both components.
    # This is equivalent to saying the sequence of pairs is sorted in non-descending order.
    # However, if we have pairs like (1, 2) and (1, 3), sorting by A gives (1, 2), (1, 3) (stable sort or arbitrary among equals).
    # But sorting by B would give (1, 2), (1, 3) as well? No, (1, 2) has B=2, (1, 3) has B=3.
    # So if pairs are distinct, there is only 1 way to arrange them to be sorted by A, and if that arrangement is also sorted by B, then it counts.
    # But what if pairs are not distinct?
    # Example: (1, 2), (1, 2). Sorted by A: (1, 2), (1, 2). Sorted by B: (1, 2), (1, 2).
    # The number of permutations of indices that result in a sequence of pairs that is non-decreasing in both A and B.
    # This is equivalent to: the sequence of pairs P' must satisfy P'[i] <= P'[i+1] (component-wise).
    # If such a sorted sequence of pairs exists, how many index permutations map to it?
    # It is the product of factorials of counts of each distinct pair.
    # But does a sorted sequence always exist? Yes, we can just sort the pairs.
    # However, we must ensure that the sorted sequence of pairs satisfies the condition that A is non-decreasing AND B is non-decreasing.
    # Since we are sorting the pairs primarily by A, if there are ties in A, we need to check if we can order the ties such that B is also non-decreasing.
    # Actually, the standard lexicographical sort (sort by A, then by B) produces a sequence where A is non-decreasing. 
    # Within groups of equal A, the sequence of B must also be non-decreasing for the whole sequence to be non-decreasing in B.
    # If in a group of equal A, the B values are not sortable to be non-decreasing (i.e., they contain duplicates, which is fine, but if they are distinct they must be in order),
    # wait. If we have (1, 3) and (1, 2). Sorted by A: both are 1. To make B non-decreasing, we must put (1, 2) then (1, 3).
    # So the unique sequence of pairs that is sorted by A and B is the one obtained by sorting pairs (A, B) lexicographically.
    # Let this sorted sequence of pairs be S.
    # If S is such that the B components are non-decreasing, then it is a valid "both sorted" sequence.
    # Note: If we sort by (A, B) lexicographically, A is non-decreasing. Is B non-decreasing?
    # Not necessarily. Example: (1, 3), (2, 2). Sorted: (1, 3), (2, 2). A: 1, 2 (ok). B: 3, 2 (not ok).
    # So we must check if the lexicographically sorted list of pairs has non-decreasing B.
    # If it does, then the number of index permutations is product of (count of each distinct pair!).
    # If it doesn't, then there are 0 permutations where both are sorted.
    
    # Step 1: Get sorted pairs
    pairs = list(zip(a, b))
    pairs.sort() # Lexicographical sort
    
    # Step 2: Check if B is non-decreasing in this sorted list
    possible_both = True
    for i in range(n - 1):
        if pairs[i][1] > pairs[i+1][1]:
            possible_both = False
            break
    
    count_both_sorted = 0
    if possible_both:
        # Calculate product of factorials of counts of identical pairs
        # We already have pair_counts
        for count in pair_counts.values():
            count_both_sorted = (count_both_sorted * fact[count]) % MOD
        # Wait, count_both_sorted was initialized to 0. Need to set it properly.
        # Recalculate:
        count_both_sorted = 1
        for count in pair_counts.values():
            count_both_sorted = (count_both_sorted * fact[count]) % MOD

    # Apply inclusion-exclusion principle
    # Good = Total - (A_sorted OR B_sorted)
    # |A U B| = |A| + |B| - |A n B|
    # Count = Total - (count_A_sorted + count_B_sorted - count_both_sorted)
    
    bad_count = (count_A_sorted + count_B_sorted - count_both_sorted) % MOD
    ans = (total_perms - bad_count + MOD) % MOD

    print(ans)

if __name__ == '__main__':
    solve()