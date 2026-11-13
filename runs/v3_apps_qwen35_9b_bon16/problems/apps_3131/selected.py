import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        K = int(next(iterator))
        A = []
        for _ in range(N):
            A.append(int(next(iterator)))
    except StopIteration:
        return

    MOD = 1000000007

    A.sort()

    total_sum = 0

    # We will count how many times each element is the maximum in a combination of K keys.
    # If we sort the array in ascending order, then for an element at index i (0-based),
    # it will be the maximum if we choose it and then choose K-1 other keys from the elements
    # with indices greater than i.
    # However, since the array may have duplicate values, we need to be careful.
    # Actually, the standard combinatorial approach works even with duplicates if we define "maximum"
    # based on the sorted position or simply by value. But note: if there are multiple keys with the same max value,
    # the problem says "it will play only the key with the largest value". If there are multiple keys with the same largest value,
    # which one is played? The problem statement implies the value is what matters, but the phrasing "the key" suggests uniqueness in selection logic?
    # Re-reading: "after pressing K keys at the same time, it will play only the key with the largest value."
    # If there are multiple keys with the same largest value, the value played is that value. The question asks for the sum of values.
    # So if we have multiple keys with the same max value in a set, the contribution to the sum is (that value) * 1 for that set.
    #
    # Let's reconsider the counting method with duplicates.
    # Standard approach for this problem (often seen in competitive programming):
    # Sort the array. For the element at index i (0-indexed in sorted array), it is the maximum in a subset of size K
    # if we pick this element and K-1 elements from the indices i+1 to N-1.
    # BUT, this logic assumes distinct values or a specific tie-breaking rule.
    # However, if there are duplicates, say values [2, 2, 4] and K=2.
    # Subsets: {2a, 2b} -> max 2. {2a, 4} -> max 4. {2b, 4} -> max 4.
    # Total sum = 2 + 4 + 4 = 10.
    # Using the index-based counting on sorted array [2, 2, 4]:
    # Index 0 (val 2): need 1 from indices >0 -> index 1 or 2.
    #   Picking index 0 and 1: max is 2 (correct).
    #   Picking index 0 and 2: max is 4 (incorrect, max should be 4, but index 0 is not the max here).
    # Wait, the logic "element at i is max if we pick it and K-1 from >i" implies that element i is strictly greater than or equal to all chosen from >i?
    # No, if we pick from >i, those elements are >= A[i]. So A[i] would NOT be the maximum unless A[i] >= all others.
    # Since the array is sorted ascending, elements at indices > i are >= A[i].
    # Therefore, A[i] can only be the maximum if we pick it and K-1 elements that are <= A[i].
    # But we are restricted to picking from the set.
    #
    # Correct Logic for Sum of Maximums:
    # Sort the array in ascending order.
    # Consider the contribution of each element as the maximum.
    # An element A[i] is the maximum of a subset if all other K-1 elements in the subset are <= A[i].
    # However, if there are duplicates, say multiple elements equal to A[i], any of them could be considered the "key" played, but the value is the same.
    # The problem asks for the sum of values. So if a subset has multiple keys with the same max value V, the value added is V.
    #
    # Let's count how many subsets have a maximum value exactly equal to X.
    # Alternatively, iterate through the sorted array and decide how many times A[i] is the maximum.
    # If we fix the maximum value to be A[i], we must choose K-1 other elements from the elements that are <= A[i].
    # BUT, to avoid double counting when there are duplicates, we can assign a canonical "representative" for the maximum.
    # Convention: In a sorted array, for a subset with maximum value V, the element at the largest index among those with value V is the one we "credit" as the maximum for counting purposes?
    # Actually, simpler approach:
    # Sort A ascending.
    # For each index i from 0 to N-1:
    #   This element A[i] is the maximum of a combination if we choose it, and choose K-1 elements from the range [0, i-1].
    #   Why? Because if we choose any element from [i+1, N-1], that element would be >= A[i], making A[i] not the unique maximum in terms of index, and since the array is sorted, A[j] >= A[i] for j > i.
    #   If there are duplicates, e.g., [2, 2, 4] sorted.
    #   i=0 (val 2): choose 0 from indices >0? No, we need K-1 from indices < i?
    #   Let's reverse the thinking.
    #   Sort ascending.
    #   If we pick a subset, the maximum is the element with the largest index in that subset.
    #   Let the subset indices be s_1 < s_2 < ... < s_K. The maximum is A[s_K].
    #   So, for a fixed index i to be the largest index in the subset (and thus provide the value A[i]),
    #   we must choose K-1 other indices from the range [0, i-1].
    #   Number of ways = C(i, K-1).
    #   Then we add A[i] * C(i, K-1) to the total.
    #
    # Let's test this logic with Sample 1: 5 3, [2, 4, 2, 3, 4]
    # Sorted: [2, 2, 3, 4, 4]
    # Indices: 0, 1, 2, 3, 4
    # i=0 (val 2): C(0, 2) = 0
    # i=1 (val 2): C(1, 2) = 0
    # i=2 (val 3): C(2, 2) = 1. Subset indices {0,1,2} -> vals {2,2,3}. Max is 3. Correct.
    # i=3 (val 4): C(3, 2) = 3. Subsets of size 2 from {0,1,2} combined with {3}.
    #   {0,1,3} -> {2,2,4} max 4
    #   {0,2,3} -> {2,3,4} max 4
    #   {1,2,3} -> {2,3,4} max 4
    # i=4 (val 4): C(4, 2) = 6. Subsets of size 2 from {0,1,2,3} combined with {4}.
    #   Wait, if we pick {3, 4} as indices, values are {4, 4}. Max is 4.
    #   Is this correct? Yes. The value is 4.
    #   Total sum = 1*3 + 3*4 + 6*4 = 3 + 12 + 24 = 39.
    # Matches Sample 1 output.
    #
    # Test Sample 2: 5 1, [1, 0, 1, 1, 1]
    # Sorted: [0, 1, 1, 1, 1]
    # K=1. We choose 0 elements from [0, i-1]. C(i, 0) = 1 for all i >= 0.
    # i=0 (0): 1 * 0 = 0
    # i=1 (1): 1 * 1 = 1
    # i=2 (1): 1 * 1 = 1
    # i=3 (1): 1 * 1 = 1
    # i=4 (1): 1 * 1 = 1
    # Total = 4. Matches Sample 2.
    #
    # Conclusion: The logic is: Sort A. Sum = sum(A[i] * C(i, K-1)) for i from K-1 to N-1.
    # We need to compute combinations C(n, r) modulo 10^9+7.
    # Since N is up to 100,000 and K is up to 50, we can precompute factorials or compute C(i, K-1) iteratively.
    # Given K is small, we can compute C(i, K-1) efficiently.
    # C(i, K-1) = i! / ((K-1)! * (i - (K-1))!)
    # Or iteratively: C(i, k) = C(i-1, k) * i / (i-k). But division modulo requires modular inverse.
    # Since K is small, we can just compute C(i, K-1) using a loop or precomputed factorials.
    # Precomputing factorials up to N is easy.

    if K > N:
        print(0)
        return

    # Precompute factorials and inverse factorials for combinations
    MOD = 1000000007
    limit = N
    fact = [1] * (limit + 1)
    inv = [1] * (limit + 1)
    
    for i in range(1, limit + 1):
        fact[i] = (fact[i-1] * i) % MOD
        
    # Modular inverse using Fermat's Little Theorem: a^(MOD-2) % MOD
    def power(a, b):
        res = 1
        a %= MOD
        while b > 0:
            if b % 2 == 1:
                res = (res * a) % MOD
            a = (a * a) % MOD
            b //= 2
        return res

    inv[limit] = power(fact[limit], MOD - 2)
    for i in range(limit - 1, -1, -1):
        inv[i] = (inv[i+1] * (i+1)) % MOD

    def nCr_mod(n, r):
        if r < 0 or r > n:
            return 0
        num = fact[n]
        den = (inv[r] * inv[n-r]) % MOD
        return (num * den) % MOD

    ans = 0
    r_needed = K - 1
    
    # We only need to iterate from i = r_needed to N-1
    for i in range(r_needed, N):
        ways = nCr_mod(i, r_needed)
        val = A[i]
        term = (ways * val) % MOD
        ans = (ans + term) % MOD

    print(ans)

if __name__ == '__main__':
    solve()