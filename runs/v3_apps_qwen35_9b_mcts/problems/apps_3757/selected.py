import sys

def solve():
    try:
        input_data = sys.stdin.read().split()
        if not input_data:
            return
        a00 = int(input_data[0])
        a01 = int(input_data[1])
        a10 = int(input_data[2])
        a11 = int(input_data[3])
    except ValueError:
        print("Impossible")
        return

    # Function to solve n*(n-1)/2 = target for non-negative integer n
    def solve_n(target):
        if target == 0:
            return 0, 1  # n could be 0 or 1, we will handle logic later
        # n^2 - n - 2*target = 0
        # discriminant = 1 + 8*target
        D = 1 + 8 * target
        sqrt_D = int(D**0.5)
        if sqrt_D * sqrt_D != D:
            return -1, -1
        n = (1 + sqrt_D) // 2
        if n * (n - 1) // 2 == target:
            return n, n
        return -1, -1

    n0_candidates, n1_candidates = solve_n(a00), solve_n(a11)

    # Determine n0 and n1
    # If a00 == 0, n0 can be 0 or 1. If a00 > 0, n0 is uniquely determined.
    # Same for n1.
    
    if n0_candidates[0] == -1:
        print("Impossible")
        return
    if n1_candidates[0] == -1:
        print("Impossible")
        return

    # Handle the ambiguity when count is 0 (n could be 0 or 1)
    # If a00 == 0, n0 can be 0 or 1.
    # If a11 == 0, n1 can be 0 or 1.
    
    possible_n0 = []
    if a00 == 0:
        possible_n0 = [0, 1]
    else:
        possible_n0 = [n0_candidates[0]]

    possible_n1 = []
    if a11 == 0:
        possible_n1 = [0, 1]
    else:
        possible_n1 = [n1_candidates[0]]

    found = False
    best_s = None

    for n0 in possible_n0:
        for n1 in possible_n1:
            # Check consistency of cross terms
            # Total pairs of (0,1) and (1,0) must sum to n0 * n1
            if a01 + a10 != n0 * n1:
                continue
            
            # Special case: if both n0 and n1 are 0, string is empty, but problem says non-empty.
            # However, if a00=0, a11=0, a01=0, a10=0, we can have "0" or "1".
            if n0 == 0 and n1 == 0:
                # This implies a00=0, a11=0, a01=0, a10=0.
                # We need a non-empty string. "0" works (n0=1, n1=0) or "1" works (n0=0, n1=1).
                # Our loops above might have picked n0=0, n1=0 which is invalid for non-empty.
                # But we are iterating possible_n0 and possible_n1 derived from a00=0, a11=0.
                # If we pick n0=0, n1=0, it fails the non-empty check implicitly if we construct empty string.
                # Let's skip this specific combination if it leads to empty string, 
                # but we must ensure we find a valid non-empty one.
                # Actually, if a00=0, a11=0, a01=0, a10=0, valid strings are "0", "1", "00", "11", etc.
                # "0" -> n0=1, n1=0. "1" -> n0=0, n1=1.
                # Our loop will try n0=0, n1=0 -> skip (empty).
                # Then try n0=1, n1=0 -> valid.
                # Then try n0=0, n1=1 -> valid.
                # Then try n0=1, n1=1 -> a01+a10 must be 1, but here 0, so invalid.
                continue

            # Now we have candidate n0, n1.
            # We need to construct a string with n0 zeros and n1 ones such that:
            # a01 = number of "01" subsequences
            # a10 = number of "10" subsequences
            # Note: a01 + a10 = n0 * n1 is already checked.
            
            # Strategy to construct lexicographically smallest string:
            # We want as many '0's as possible at the beginning.
            # Consider the structure: k zeros, then all n1 ones, then (n0 - k) zeros.
            # In this structure:
            # - The "01" subsequences come from the first k zeros paired with all n1 ones.
            #   Count = k * n1.
            # - The "10" subsequences come from all n1 ones paired with the remaining (n0 - k) zeros.
            #   Count = n1 * (n0 - k).
            # We need k * n1 = a01.
            # So k = a01 / n1.
            # This requires n1 > 0. If n1 == 0, then a01 must be 0 and a10 must be 0.
            # If n1 == 0, then we just have n0 zeros. String is "0"*n0.
            # If n0 == 0, then we just have n1 ones. String is "1"*n1.
            
            if n1 == 0:
                if a01 != 0 or a10 != 0:
                    continue
                s = "0" * n0
                if len(s) > 0:
                    best_s = s
                    found = True
                    break
            elif n0 == 0:
                if a01 != 0 or a10 != 0:
                    continue
                s = "1" * n1
                if len(s) > 0:
                    best_s = s
                    found = True
                    break
            else:
                # n1 > 0 and n0 > 0
                if a01 % n1 != 0:
                    continue
                k = a01 // n1
                if k < 0 or k > n0:
                    continue
                
                # Construct string: k zeros, n1 ones, (n0-k) zeros
                s = "0" * k + "1" * n1 + "0" * (n0 - k)
                if len(s) > 0:
                    best_s = s
                    found = True
                    break
        if found:
            break

    if found:
        print(best_s)
    else:
        print("Impossible")

if __name__ == "__main__":
    solve()