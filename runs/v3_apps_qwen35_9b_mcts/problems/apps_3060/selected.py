import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    n = int(input_data[0])
    k = int(input_data[1])

    # We need to find the k-th lexicographically smallest sequence a_1, ..., a_{n-1}
    # where 1 <= a_i <= n-1
    # and for any contiguous subsegment, the sum is not divisible by n.
    #
    # Key Insight:
    # Let P[i] be the prefix sum a_1 + ... + a_i, with P[0] = 0.
    # The condition "no contiguous subsegment sum is divisible by n" is equivalent to:
    # For all 0 <= i < j <= n-1, (P[j] - P[i]) % n != 0.
    # This implies that all prefix sums P[0], P[1], ..., P[n-1] must be distinct modulo n.
    # Since there are exactly n possible residues modulo n (0 to n-1) and we have n prefix sums,
    # the set {P[0], P[1], ..., P[n-1]} must be a permutation of {0, 1, ..., n-1}.
    #
    # We know P[0] = 0.
    # Therefore, P[1], P[2], ..., P[n-1] must be a permutation of {1, 2, ..., n-1}.
    # Also, a_i = P[i] - P[i-1] (modulo n arithmetic, but we need actual values 1..n-1).
    # Specifically, a_i = (P[i] - P[i-1]) if P[i] > P[i-1] else (P[i] - P[i-1] + n).
    # Since a_i must be in [1, n-1], this mapping is bijective between valid permutations of residues
    # and valid sequences of petals.
    #
    # The problem reduces to: Find the k-th lexicographically smallest sequence a_1, ..., a_{n-1}.
    # This corresponds to finding a permutation of {1, ..., n-1} for P[1], ..., P[n-1] such that
    # the resulting sequence a is lexicographically minimized, and we pick the k-th such sequence.
    #
    # However, lexicographical order on 'a' is NOT the same as lexicographical order on 'P'.
    # We must iterate on a_1, then a_2, etc.
    #
    # Algorithm:
    # We build the sequence a_1, a_2, ..., a_{n-1} digit by digit.
    # At step i (1-indexed), we try possible values for a_i from 1 to n-1.
    # Let current prefix sum residue be cur = P[i-1].
    # If we choose a_i, then new prefix sum residue next_p = (cur + a_i) % n.
    # We must ensure that next_p has not been used in {P[0], ..., P[i-1]}.
    # Additionally, we need to count how many ways we can complete the remaining n-1-i positions
    # given the set of used residues so far.
    #
    # The number of ways to complete the sequence depends ONLY on the number of remaining unused residues.
    # Why? Because at each subsequent step j, we can choose any unused residue r as P[j],
    # and set a_{j+1} = (r - P[j]) mod n (adjusted to be in 1..n-1).
    # Since any unused residue is valid (it hasn't been used before, so no collision with previous P's),
    # and we just need to pick a permutation of the remaining unused residues for the future P's.
    # The number of ways to arrange m unused residues in m positions is m!.
    #
    # So, at any point, if we have 'm' unused residues available for the future prefix sums,
    # the number of valid completions is m!.
    #
    # Steps:
    # 1. Initialize used_residues = {0}.
    # 2. current_p = 0.
    # 3. For position i from 1 to n-1:
    #    m = number of unused residues = (n-1) - (i-1) = n - i.
    #    Wait, actually:
    #    Before choosing a_i, we have used i-1 residues (including P[0]=0).
    #    Total residues = n.
    #    Unused count = n - (i-1) - 1? No.
    #    Let's re-evaluate.
    #    We need to choose P[1], P[2], ..., P[n-1] which are a permutation of {1, ..., n-1}.
    #    At step i (choosing a_i), we determine P[i].
    #    P[i] = (P[i-1] + a_i) % n.
    #    We need P[i] to be in the set of unused residues from {1, ..., n-1}.
    #    Let U be the set of unused residues from {1, ..., n-1}. Initially U = {1, ..., n-1}.
    #    Size of U is n-1.
    #    At step i (1 to n-1):
    #      We try a_i in 1..n-1.
    #      next_p = (current_p + a_i) % n.
    #      If next_p is in U:
    #         We tentatively pick this a_i.
    #         How many completions?
    #         We have used one more residue (next_p). Remaining unused in U: |U| - 1.
    #         The number of ways to arrange the remaining |U|-1 residues for the remaining positions
    #         is (|U|-1)!.
    #         Let count = (|U|-1)!.
    #         If k <= count:
    #            We select this a_i.
    #            Update current_p = next_p.
    #            Remove next_p from U.
    #            Break inner loop (move to next position).
    #         Else:
    #            k -= count.
    #            Try next a_i.
    #      Else:
    #         This a_i is invalid (collision), skip.
    #
    # Precompute factorials up to n-1. Since n <= 1000, we can precompute.
    # Note: k can be up to 10^18, so we need 64-bit integers. Python handles this automatically.
    # Factorials grow very fast. 20! is ~2e18. So for n > 21, (n-1)! is huge, but k is limited to 10^18.
    # However, the problem guarantees k valid sequences exist.
    # We just need to be careful with large factorials. If (m-1)! >= k, we might not need the exact huge value,
    # but since we subtract, we need the exact value if it's <= k. If it's > k, we just know it's big enough.
    # Actually, since k <= 10^18, any factorial > 10^18 can be treated as infinity for comparison purposes,
    # but we must subtract correctly.
    # Wait, if count > k, we pick it. If count < k, we subtract.
    # So we need the exact value of count if count <= k. If count > k, we don't need the exact huge number,
    # we just know it's larger than k. But to be safe and simple, we can cap factorials at k+1.
    
    max_k = k
    fact = [1] * n
    for i in range(2, n):
        val = fact[i-1] * i
        if val > max_k:
            val = max_k + 1
        fact[i] = val

    result = []
    used = {0}
    current_p = 0
    # Set of available residues for P[1]...P[n-1]
    available = set(range(1, n))

    for i in range(1, n):
        # Number of remaining positions after this one: (n-1) - i
        # Number of available residues BEFORE picking this one: len(available)
        # If we pick a valid next_p, remaining available will be len(available) - 1.
        # The number of ways to complete is (len(available) - 1)!
        
        m = len(available)
        # If m == 0, something is wrong, but loop runs n-1 times and we start with n-1 available.
        
        # Calculate ways for the next step
        # ways = fact[m-1]
        # But if m-1 is large, fact[m-1] might be capped.
        # If fact[m-1] is capped (meaning > k), then any valid choice will satisfy k <= count.
        
        ways = fact[m-1]
        
        # Try a_i from 1 to n-1
        found = False
        for a in range(1, n):
            next_p = (current_p + a) % n
            if next_p in available:
                # Valid move
                if k <= ways:
                    # Select this a
                    result.append(a)
                    current_p = next_p
                    available.remove(next_p)
                    found = True
                    break
                else:
                    k -= ways
            # else: invalid move, continue
        
        if not found:
            # This should not happen given problem constraints
            pass

    print(*(result))

if __name__ == "__main__":
    solve()