import sys

# Increase recursion depth just in case, though we use iterative approach
sys.setrecursionlimit(2000)

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

    # Precompute factorials and inverse factorials
    fact = [1] * (n + 1)
    inv = [1] * (n + 1)
    
    for i in range(1, n + 1):
        fact[i] = (fact[i-1] * i) % MOD
        
    inv[n] = pow(fact[n], MOD - 2, MOD)
    for i in range(n - 1, -1, -1):
        inv[i] = (inv[i+1] * (i + 1)) % MOD

    def count_sorted_by_first():
        # Count permutations where the sequence is sorted by first elements (non-descending)
        # If there are duplicate 'a' values, any permutation of indices within those groups is valid.
        # The number of such permutations is the product of factorials of the counts of each distinct 'a' value.
        
        # We need to count frequencies of each 'a' value
        # Since a_i <= n, we can use a frequency array or a dict
        freq = {}
        for x in a:
            freq[x] = freq.get(x, 0) + 1
        
        ans = 1
        for count in freq.values():
            ans = (ans * fact[count]) % MOD
        return ans

    def count_sorted_by_second():
        # Count permutations where the sequence is sorted by second elements (non-descending)
        freq = {}
        for x in b:
            freq[x] = freq.get(x, 0) + 1
        
        ans = 1
        for count in freq.values():
            ans = (ans * fact[count]) % MOD
        return ans

    def count_sorted_by_both():
        # Count permutations where the sequence is sorted by first elements AND second elements.
        # This means the sequence of pairs must be sorted lexicographically (by a, then by b).
        # However, the condition "sorted by first" and "sorted by second" implies:
        # 1. a_1 <= a_2 <= ... <= a_n
        # 2. b_1 <= b_2 <= ... <= b_n
        # If we sort the original pairs lexicographically, we get a candidate sequence.
        # We must check if this candidate sequence also satisfies the non-descending condition for 'b'.
        # If it does, then any permutation of indices that maps to this sorted value sequence is valid.
        # The number of such permutations is the product of factorials of the counts of each distinct pair (a, b).
        
        # Create list of pairs with original indices to handle duplicates correctly if needed, 
        # but actually we just need the counts of distinct pairs.
        # Let's sort the pairs based on (a, b).
        pairs = []
        for i in range(n):
            pairs.append((a[i], b[i]))
        
        pairs.sort()
        
        # Check if 'b' is non-descending in the sorted pairs
        is_b_sorted = True
        for i in range(1, n):
            if pairs[i][1] < pairs[i-1][1]:
                is_b_sorted = False
                break
        
        if not is_b_sorted:
            return 0
        
        # If b is sorted, we count permutations that result in this specific sorted sequence of pairs.
        # Since the pairs might be identical, we group by (a, b) and multiply factorials of counts.
        freq = {}
        for x, y in pairs:
            pair = (x, y)
            freq[pair] = freq.get(pair, 0) + 1
        
        ans = 1
        for count in freq.values():
            ans = (ans * fact[count]) % MOD
        return ans

    # Total permutations
    total = fact[n]
    
    # Count bad permutations
    bad_first = count_sorted_by_first()
    bad_second = count_sorted_by_second()
    bad_both = count_sorted_by_both()
    
    # By Inclusion-Exclusion Principle:
    # |A U B| = |A| + |B| - |A n B|
    # Good = Total - |A U B|
    
    bad_union = (bad_first + bad_second - bad_both) % MOD
    good = (total - bad_union) % MOD
    
    # Ensure positive result
    if good < 0:
        good += MOD
        
    print(good)

if __name__ == '__main__':
    solve()