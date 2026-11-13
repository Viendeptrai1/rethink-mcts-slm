import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    n = int(input_data[0])
    k = int(input_data[1])

    # We need to find the k-th lexicographically smallest sequence a_1, ..., a_{n-1}
    # where 1 <= a_i <= n-1
    # and for every contiguous subsegment, the sum is NOT divisible by n.
    #
    # Let prefix sums be P_0 = 0, P_i = (a_1 + ... + a_i) mod n.
    # The condition "no contiguous subsegment sum is divisible by n" means:
    # For any 0 <= i < j <= n-1, (P_j - P_i) mod n != 0  => P_j != P_i.
    # Since there are n possible residues (0 to n-1) and we have n indices (0 to n-1),
    # the only way to have all P_i distinct is to have P_i be a permutation of 0..n-1.
    #
    # Constraints on a_i:
    # a_i = (P_i - P_{i-1}) mod n.
    # We require 1 <= a_i <= n-1.
    # This implies (P_i - P_{i-1}) mod n != 0, so P_i != P_{i-1}.
    # But since all P_i must be distinct anyway, this is automatically satisfied if all P_i are distinct.
    #
    # So the problem reduces to:
    # Find the k-th lexicographically smallest sequence of prefix sums P_0, P_1, ..., P_{n-1}
    # such that:
    # 1. P_0 = 0
    # 2. All P_i are distinct elements of {0, 1, ..., n-1}
    # 3. The derived a_i = (P_i - P_{i-1}) mod n satisfies 1 <= a_i <= n-1.
    #    Note: a_i = 0 iff P_i = P_{i-1}, which is forbidden by distinctness.
    #    Also a_i = n is impossible since mod n gives 0..n-1, and 0 is excluded by distinctness.
    #    So any permutation starting with 0 yields valid a_i in [1, n-1].
    #
    # Lexicographical order of sequences a_1, ..., a_{n-1} corresponds to:
    # Comparing a_1 first, then a_2, etc.
    # a_1 = (P_1 - P_0) mod n = P_1 mod n (since P_0=0).
    # So smaller a_1 means smaller P_1.
    # Given P_0, P_1, ..., P_{i-1}, we choose P_i such that:
    # - P_i is not in {P_0, ..., P_{i-1}}
    # - a_i = (P_i - P_{i-1}) mod n is minimized (to get lexicographically smallest next element)
    # But we are enumerating the k-th sequence, so we need to count how many valid completions exist
    # for each choice of P_i.
    #
    # Actually, the lexicographical order is on the sequence a.
    # a_1 = P_1.
    # a_2 = (P_2 - P_1) mod n.
    # ...
    # To generate the k-th sequence:
    # Iterate position i from 1 to n-1.
    # Try possible values for a_i in increasing order (1 to n-1).
    # For a fixed a_i, P_i = (P_{i-1} + a_i) mod n.
    # Check if P_i is already used.
    # If not used, count how many ways to complete the rest of the sequence (positions i+1 to n-1).
    # If k <= count, then this a_i is correct; move to next position with new P_i and used set.
    # Else, subtract count from k and try next a_i.
    #
    # Counting completions:
    # We have m = n - i positions left to fill (from i to n-1, so n-1 - i + 1 = n-i steps? 
    # Wait: we are at step i (1-indexed), having chosen P_0...P_{i-1}. We need to choose P_i...P_{n-1}.
    # Number of remaining positions to choose: (n-1) - i + 1 = n - i.
    # We have (n - i) residues left to assign (since i residues are used: P_0...P_{i-1}).
    # Let R = n - i (number of remaining steps).
    # Let U = set of used residues (size i).
    # Let S = set of available residues (size n - i).
    # We need to form a sequence P_i, P_{i+1}, ..., P_{n-1} using each element of S exactly once.
    # The number of such sequences is simply the number of permutations of S, which is (n-i)!.
    # BUT: Is there any additional constraint?
    # The constraint is only that P_j != P_k for j != k, which is satisfied by using a permutation.
    # And a_j = (P_j - P_{j-1}) mod n must be in [1, n-1].
    # Since all P are distinct, a_j is never 0 mod n, so a_j is in [1, n-1].
    # Therefore, ANY permutation of the remaining residues is valid.
    #
    # So the number of completions given we have chosen i residues so far (including P_0) is (n - i)!.
    # This is independent of which specific residues are used, only the count matters.
    #
    # Algorithm:
    # used = {0}
    # current_P = 0
    # result = []
    # for i from 1 to n-1:
    #   remaining_count = n - i
    #   factorial_remaining = factorial(remaining_count)
    #   for a in 1..n-1:
    #     next_P = (current_P + a) % n
    #     if next_P in used: continue
    #     count = factorial_remaining
    #     if k <= count:
    #       result.append(a)
    #       used.add(next_P)
    #       current_P = next_P
    #       break
    #     else:
    #       k -= count
    #
    # Precompute factorials up to n.
    # n <= 1000, so factorials can be huge, but k <= 10^18.
    # We only need factorials until they exceed k. Since 20! > 10^18, we can cap factorials at k+1.

    fact = [1] * (n + 1)
    for i in range(2, n + 1):
        val = fact[i-1] * i
        if val > 10**18 + 7:
            val = 10**18 + 7
        fact[i] = val

    used = {0}
    current_P = 0
    result = []

    for i in range(1, n):
        remaining_steps = n - i
        count_per_choice = fact[remaining_steps]
        
        chosen = False
        for a in range(1, n):
            next_P = (current_P + a) % n
            if next_P in used:
                continue
            if k <= count_per_choice:
                result.append(a)
                used.add(next_P)
                current_P = next_P
                chosen = True
                break
            else:
                k -= count_per_choice
        if not chosen:
            # Should not happen given problem guarantee
            pass

    print(*(result))

if __name__ == "__main__":
    solve()