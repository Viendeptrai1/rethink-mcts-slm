import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    n = int(input_data[0])
    k = int(input_data[1])

    # If n = 2, the only valid sequence of length 1 is [1] because 1 is not a multiple of 2.
    # Any k > 1 would be invalid, but the problem guarantees k is valid.
    if n == 2:
        print(1)
        return

    # We need to find the k-th lexicographically smallest sequence a_1, ..., a_{n-1}
    # such that 1 <= a_i <= n-1 and no non-empty contiguous subsequence sum is divisible by n.
    # This condition is equivalent to: all prefix sums modulo n must be distinct.
    # Let P_i = (a_1 + ... + a_i) % n.
    # P_0 = 0.
    # The condition "no contiguous subsequence sum is 0 mod n" means P_j - P_i != 0 mod n for j > i.
    # This implies all P_0, P_1, ..., P_{n-1} must be distinct.
    # Since there are n possible residues (0 to n-1) and we have n values (P_0 to P_{n-1}),
    # the set {P_0, ..., P_{n-1}} must be exactly {0, 1, ..., n-1}.
    # Thus, P_1, ..., P_{n-1} is a permutation of {1, ..., n-1}.
    # Also, a_i = (P_i - P_{i-1}) mod n. Since 1 <= a_i <= n-1, we must have P_i != P_{i-1},
    # which is already guaranteed by the distinctness.
    # Specifically, a_i = (P_i - P_{i-1}) if P_i > P_{i-1} else n - (P_{i-1} - P_i).
    # Actually, simply a_i = (P_i - P_{i-1}) % n. If result is 0, it means P_i = P_{i-1}, which is impossible.
    # So a_i is determined by the transition from P_{i-1} to P_i.

    # The problem reduces to finding the k-th permutation of {1, 2, ..., n-1} (for P_1 to P_{n-1})
    # such that we construct the sequence lexicographically based on a_1, a_2, ...
    # Note: Lexicographical order on the sequence (a_1, a_2, ...) is NOT the same as lexicographical order on (P_1, P_2, ...).
    # We need to iterate positions i from 1 to n-1, and for each position, try possible values of a_i (1 to n-1)
    # in increasing order, check if a valid completion exists, and subtract counts from k.

    # Available residues for P_i: {0, 1, ..., n-1} \ {P_0, ..., P_{i-1}}
    # P_0 is fixed at 0.
    # Let used = {0}.
    # At step i (1 to n-1):
    #   Try a in 1..n-1:
    #     p_next = (prev_p + a) % n
    #     If p_next is in used, skip.
    #     If p_next is not in used, then this choice of a leads to a valid prefix (residue-wise).
    #     But we also need to know how many ways to complete the sequence from state (i, used_set, prev_p).
    #     This looks like counting linear extensions or Hamiltonian paths in a specific graph, which is hard for large n.
    #     HOWEVER, notice the structure.
    #     We are building a path 0 -> P_1 -> P_2 -> ... -> P_{n-1} visiting every node exactly once.
    #     This is a Hamiltonian path starting at 0 in the complete graph of residues 0..n-1, with edge weights being the steps.
    #     But the lexicographical order is on the edge weights (a_i), not the nodes (P_i).
    #
    # Let's re-evaluate the constraints. n <= 1000. k <= 10^18.
    # The number of such sequences is (n-1)! because P_1...P_{n-1} can be any permutation of 1..n-1.
    # (n-1)! for n=1000 is huge, so k=10^18 is small compared to the total count.
    # But we cannot compute factorials beyond ~20! easily without big integers, and Python handles them, but O(n) per digit is O(n^2) total which is fine for n=1000.
    # Wait, the number of permutations is (n-1)!. For n=1000, this is massive.
    # The algorithm needs to be O(n) or O(n log k).
    #
    # Key Insight:
    # The sequence a determines P. P_0=0. P_i = (P_{i-1} + a_i) % n.
    # The condition is that P_1, ..., P_{n-1} are a permutation of 1, ..., n-1.
    # We want the k-th lexicographical sequence a.
    # We determine a_1, then a_2, etc.
    # For a fixed prefix of P's, how many completions exist?
    # Once we pick P_1, P_2, ..., P_{i}, the remaining set of residues is fixed.
    # We need to order the remaining n-1-i residues in some way such that the transitions are valid?
    # Actually, ANY ordering of the remaining residues works?
    # Let's check. Suppose we have used a set of residues S (including 0). We are at prev_p.
    # We need to visit all remaining nodes in {0..n-1} \ S exactly once, starting from prev_p.
    # Since the graph is a complete graph (any transition is allowed as long as target is unused),
    # ANY permutation of the remaining nodes is a valid path.
    # Therefore, if we have m remaining nodes to visit, there are m! ways to complete the sequence.
    #
    # So the counting is very simple:
    # At step i (from 1 to n-1):
    #   Current used set U (initially {0}).
    #   Current residue p = P_{i-1} (initially 0).
    #   Number of remaining nodes m = (n-1) - (i-1) = n - i.
    #   We try a in 1, 2, ..., n-1:
    #     next_p = (p + a) % n
    #     if next_p in U: continue
    #     count = (m - 1)!  (since we fix next_p, we have m-1 nodes left to permute)
    #     if k <= count:
    #        a_i = a
    #        update U, p
    #        break
    #     else:
    #        k -= count
    #
    # Complexity:
    # Outer loop n times. Inner loop up to n times. Factorial lookup O(1) with precomputation.
    # Total O(n^2). With n=1000, 10^6 ops, perfectly fine.
    # k up to 10^18, factorials up to 999! are huge but Python handles arbitrary precision integers.
    # However, computing 1000! might be slightly slow if done repeatedly?
    # Precompute factorials up to n.
    # Also, note that if k is larger than total (n-1)!, the input guarantee says it won't happen.
    # But wait, is the number of sequences exactly (n-1)!?
    # Yes, because P_1...P_{n-1} can be any permutation of 1..n-1, and a_i is uniquely determined.
    # And any permutation yields a valid a_i in 1..n-1 (since P_i != P_{i-1}).
    #
    # One edge case: n=2. Length 1. Permutation of {1}. Only [1]. (2-1)! = 1. Correct.
    # Example 1: n=4, k=3.
    # Permutations of {1,2,3} for P_1, P_2, P_3.
    # Total 3! = 6.
    # We need 3rd.
    # Step 1: p=0, used={0}, m=3.
    # Try a=1: next_p=1. Not in used. Count = 2! = 2.
    #   k=3 > 2, so k becomes 3-2=1. Skip a=1.
    # Try a=2: next_p=2. Not in used. Count = 2.
    #   k=1 <= 2. Select a=2.
    #   used={0,2}, p=2, remaining m=2.
    # Step 2: p=2, used={0,2}.
    # Try a=1: next_p=(2+1)%4=3. Not in used. Count = 1! = 1.
    #   k=1 <= 1. Select a=1.
    #   used={0,2,3}, p=3, remaining m=1.
    # Step 3: p=3, used={0,2,3}.
    # Try a=1: next_p=0 (used).
    # Try a=2: next_p=1 (not used). Count = 0! = 1.
    #   k=1 <= 1. Select a=2.
    # Result: 2, 1, 2. Matches Sample 1.
    #
    # Example 2: n=2, k=1.
    # Step 1: p=0, used={0}, m=1.
    # Try a=1: next_p=1. Not used. Count=0!=1.
    #   k=1 <= 1. Select a=1.
    # Result: 1. Matches Sample 2.
    #
    # Example 3: n=5, k=22.
    # Total 4! = 24. k=22.
    # Step 1: p=0, used={0}, m=4.
    # a=1: next=1, count=6. k=22>6 -> k=16.
    # a=2: next=2, count=6. k=16>6 -> k=10.
    # a=3: next=3, count=6. k=10>6 -> k=4.
    # a=4: next=4, count=6. k=4<=6 -> pick 4.
    #   used={0,4}, p=4, m=3.
    # Step 2: p=4, used={0,4}.
    # a=1: next=0 (used).
    # a=2: next=1. Count=2!=2. k=4>2 -> k=2.
    # a=3: next=2. Count=2. k=2<=2 -> pick 3.
    #   used={0,4,2}, p=(4+3)%5=2, m=2.
    # Step 3: p=2, used={0,4,2}.
    # a=1: next=3. Count=1. k=2>1 -> k=1.
    # a=2: next=4 (used).
    # a=3: next=0 (used).
    # a=4: next=1. Count=1. k=1<=1 -> pick 4.
    #   used={0,4,2,1}, p=(2+4)%5=1, m=1.
    # Step 4: p=1, used={0,4,2,1}.
    # Only 3 left? No, residues 0,1,2,3,4. Used 0,1,2,4. Missing 3.
    # Try a=1: next=2 (used).
    # a=2: next=3. Count=1. k=1<=1 -> pick 2.
    # Result: 4, 3, 4, 2. Matches Sample 3.

    # Precompute factorials
    fact = [1] * (n + 1)
    for i in range(2, n + 1):
        fact[i] = fact[i-1] * i

    used = {0}
    current_p = 0
    result = []
    
    # We need to select n-1 numbers
    for i in range(1, n):
        # Number of remaining nodes to visit after this step
        # We are at step i (1-indexed), we are about to choose a_i.
        # After choosing a_i, we will have visited i nodes (0 to i).
        # Remaining nodes to visit: (n-1) - i.
        # Let rem = n - 1 - i.
        # The number of ways to complete the path once we pick a valid next_p is rem!.
        
        rem = n - 1 - i
        current_count = fact[rem]
        
        found = False
        for a in range(1, n):
            next_p = (current_p + a) % n
            if next_p in used:
                continue
            
            # This choice is valid structurally.
            # Number of completions
            ways = current_count
            
            if k <= ways:
                result.append(a)
                used.add(next_p)
                current_p = next_p
                found = True
                break
            else:
                k -= ways
        
        if not found:
            # This should not happen given the problem statement guarantees
            break
            
    print(*(result))

if __name__ == '__main__':
    solve()