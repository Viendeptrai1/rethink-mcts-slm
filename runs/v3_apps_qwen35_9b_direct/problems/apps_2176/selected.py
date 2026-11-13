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

    # Helper function to check if a list is sorted in non-descending order
    def is_sorted(arr):
        for i in range(len(arr) - 1):
            if arr[i] > arr[i+1]:
                return False
        return True

    # Count permutations where the sequence is sorted by first elements
    # This happens if we pick indices such that a[p[0]] <= a[p[1]] <= ... <= a[p[n-1]]
    # The number of such permutations is the product of factorials of counts of identical values in 'a'
    # But wait, the problem asks for permutations of the *sequence* s.
    # If there are duplicate pairs, swapping identical pairs results in the same sequence.
    # However, the problem defines a permutation p as a sequence of distinct integers 1..n.
    # So even if s[i] == s[j], swapping them (changing p) creates a different permutation p,
    # but the resulting sequence s' might be identical.
    # The question asks for the number of permutations p such that the resulting sequence is GOOD.
    # So we count valid p's.
    
    # Total permutations = n!
    # Bad permutations = (Permutations sorted by a) + (Permutations sorted by b) - (Permutations sorted by both)
    
    # Let's calculate:
    # 1. Count permutations that result in a sequence sorted by 'a'
    #    To form a sequence sorted by 'a', we must arrange the indices such that the corresponding 'a' values are non-decreasing.
    #    If there are duplicate values in 'a', say value x appears k times, then the k indices corresponding to x can be arranged in k! ways among themselves without changing the sorted order of 'a'.
    #    So, count_a = product(factorial(count of each distinct value in a))
    
    # 2. Similarly for 'b': count_b = product(factorial(count of each distinct value in b))
    
    # 3. For both: count_both = product(factorial(count of each distinct pair (a, b)))
    #    Because if we sort by both, the sequence must be sorted by 'a' AND 'b'.
    #    If two pairs are identical (a_i, b_i) == (a_j, b_j), they can be swapped freely.
    #    If (a_i, b_i) < (a_j, b_j) lexicographically, they must appear in that order.
    #    So the number of ways to arrange indices to get a sequence sorted by both is the product of factorials of counts of identical pairs.
    
    # Precompute factorials
    fact = [1] * (n + 1)
    for i in range(2, n + 1):
        fact[i] = (fact[i-1] * i) % MOD

    # Count frequencies in a
    from collections import Counter
    cnt_a = Counter(a)
    count_a = 1
    for c in cnt_a.values():
        count_a = (count_a * fact[c]) % MOD

    # Count frequencies in b
    cnt_b = Counter(b)
    count_b = 1
    for c in cnt_b.values():
        count_b = (count_b * fact[c]) % MOD

    # Count frequencies of pairs (a, b)
    cnt_pairs = Counter(zip(a, b))
    count_both = 1
    for c in cnt_pairs.values():
        count_both = (count_both * fact[c]) % MOD

    # Total permutations
    total = fact[n]

    # By Inclusion-Exclusion Principle:
    # Good = Total - (Sorted by a OR Sorted by b)
    # Sorted by a OR Sorted by b = Sorted by a + Sorted by b - Sorted by both
    # Good = Total - (count_a + count_b - count_both)
    
    bad_count = (count_a + count_b - count_both) % MOD
    ans = (total - bad_count + MOD) % MOD

    print(ans)

if __name__ == '__main__':
    solve()