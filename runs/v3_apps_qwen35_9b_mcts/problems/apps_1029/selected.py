import sys

def solve():
    s = sys.stdin.read().strip()
    if not s:
        return
    
    n = len(s)
    
    # We need to find the maximum number of original elements.
    # Each operation takes two numbers a and b (where a >= b) and replaces them with concat(a, b).
    # This reduces the count of numbers by 1 (2 removed, 1 added).
    # To get from k numbers to 1 number, we need exactly k-1 operations.
    # However, the constraint is that at each step, the first number must be >= the second.
    # Also, the final number p is formed by a specific sequence of concatenations.
    #
    # Key Insight:
    # The process is reversible in terms of structure but constrained by values.
    # If we reverse the process, we start with p and split it into two parts (left, right) such that:
    # 1. left >= right (numerically)
    # 2. The split point corresponds to a valid concatenation boundary.
    #
    # However, a simpler observation for the maximum count:
    # The maximum number of elements is achieved when we make the "cost" of each operation minimal in terms of digit consumption relative to the count increase.
    # Actually, let's look at the reverse process:
    # Start with string S = p.
    # In one reverse step, we split S into A and B (S = A + B) such that int(A) >= int(B).
    # Then we replace S with {A, B}. The count increases by 1.
    # We want to maximize the total count, so we want to maximize the number of reverse steps.
    #
    # Is it always possible to split?
    # Consider the last digit. If we split off the last digit as B, then B is a single digit d (1-9, since no leading zeros and positive integers).
    # Then A = S[:-1]. We need int(A) >= d.
    # Since S has no leading zeros, if len(S) > 1, int(A) >= 10^(len(A)-1).
    # If len(A) >= 1, int(A) >= 1.
    # If len(A) >= 2, int(A) >= 10, which is >= any single digit d.
    # If len(A) == 1, then A is a single digit. We need A >= B.
    #
    # Strategy:
    # To maximize the number of splits, we should try to make the smallest possible valid B at each step.
    # The smallest possible positive integer without leading zeros is a single digit (1-9).
    # Can we always split off the last digit?
    # Let S be the current string. Let B = S[-1] (as a string). Let A = S[:-1].
    # Condition: int(A) >= int(B).
    # Case 1: len(A) >= 2. Then int(A) >= 10. Since B is a single digit (<=9), 10 >= B is always true.
    # So if the current string has length >= 3, we can always split off the last digit.
    # Case 2: len(A) == 1. Then A and B are both single digits. We need A >= B.
    # If A < B, we cannot split off the last digit.
    # Case 3: len(A) == 0. This means S has length 1. We stop.
    #
    # Algorithm:
    # Start with count = 1 (the final single number).
    # While len(S) > 1:
    #   Try to split off the last digit as B.
    #   If len(S) >= 3: Always valid. Split. count += 1. S = S[:-1].
    #   If len(S) == 2: Check if S[0] >= S[1]. If yes, split. count += 1. S = S[0]. Else, stop.
    #
    # Wait, is it possible that splitting off the last digit is not optimal?
    # Suppose S = "10". Split off '0'? B='0'. But problem says positive integers. B cannot be 0.
    # Ah, the input p doesn't contain leading zeros, but intermediate numbers?
    # "originally the array could contain only positive integers".
    # "concat(x, y) ... adding number y to the end".
    # If y was 10, concat(5, 10) = 510.
    # If we reverse 510, we could split into 5 and 10.
    # But if we split 510 into 51 and 0, 0 is not positive.
    # So B must be a valid positive integer representation (no leading zeros, value > 0).
    # Since we are splitting a string S into A and B, B = S[k:].
    # B cannot have leading zeros unless B is "0", but 0 is not positive.
    # So B cannot start with '0' unless B is just "0" which is invalid.
    # Actually, if B starts with '0', it's invalid.
    # So we can only split at positions where the suffix does not start with '0'.
    #
    # Refined Algorithm:
    # Current string S.
    # We want to find a split point k (1 <= k < len(S)) such that:
    # 1. S[k] != '0' (to ensure B has no leading zero, since B is positive)
    # 2. int(S[:k]) >= int(S[k:])
    # We want to maximize the number of steps.
    # Greedy approach: To maximize steps, we want to make the suffix B as small as possible in terms of "value reduction" or simply try to peel off the smallest valid B.
    # The smallest valid positive integers are single digits 1-9.
    # So we prefer B to be a single digit if possible.
    #
    # Let's trace:
    # If len(S) >= 3:
    #   We can try B = S[-1]. Since len(S) >= 3, len(A) >= 2, so int(A) >= 10.
    #   B is a single digit. Since S has no leading zeros, and we are taking the last digit, B is just a digit.
    #   Is B positive? Yes, digits 1-9 are positive. What if the last digit is '0'?
    #   If S ends with '0', then B='0', which is not positive. So we cannot split off a '0' as the last element if it stands alone.
    #   However, if S ends with '0', maybe we can split off '10'?
    #   Example: S = "100".
    #   Option 1: B='0' (invalid).
    #   Option 2: B='00' (invalid, leading zero).
    #   Option 3: B='00' is invalid.
    #   Wait, if S="100", can we split?
    #   Splits:
    #     k=1: A="1", B="00" -> B invalid (leading zero).
    #     k=2: A="10", B="0" -> B invalid (0 not positive).
    #   So "100" cannot be split?
    #   But wait, the example 10000000005 -> 2.
    #   S = "10000000005".
    #   Last digit '5'. B="5". A="1000000000". 1000000000 >= 5. Valid.
    #   Result count = 2.
    #   What about "100"?
    #   If we have "100", can we get it from {10, 0}? No, 0 not allowed.
    #   From {1, 00}? No.
    #   From {100}? Count 1.
    #   So if we encounter a '0' at the end, we might be stuck if we can't form a valid B.
    #
    # Let's re-evaluate the condition for splitting off the last digit.
    # If S[-1] != '0', then B = S[-1] is a valid positive integer (1-9).
    # If len(S) >= 3, int(S[:-1]) >= 10 > 9 >= B. So valid.
    # If len(S) == 2 and S[-1] != '0':
    #   Check S[0] >= S[1]. If yes, split.
    # If S[-1] == '0':
    #   We cannot split off just '0'.
    #   We must try longer suffixes.
    #   Try B = S[-2:] (last 2 chars).
    #   If S[-2] == '0', then B starts with '0', invalid.
    #   So we need to find the smallest k such that S[k] != '0' and int(S[:k]) >= int(S[k:]).
    #   To maximize total splits, we want the smallest possible B (in terms of length? or value?).
    #   Actually, each split increases count by 1. We just need to find ONE valid split to continue.
    #   Does the choice of split affect future possibilities?
    #   Yes. If we split into A and B, the next step is on A.
    #   We want to keep A as "rich" as possible to allow more splits later.
    #   This suggests we should make B as small as possible (shortest length, then smallest value).
    #   Why? Because A = S[:-len(B)]. The longer B is, the shorter A is.
    #   Shorter A has fewer digits, making it harder to satisfy the >= condition for future splits.
    #   So the greedy strategy: Find the shortest valid suffix B.
    #
    # Algorithm Refined:
    # count = 1
    # while len(S) > 1:
    #   found = False
    #   # Try all possible split points k from 1 to len(S)-1
    #   # We want the smallest k (shortest B) that is valid.
    #   # Validity:
    #   # 1. S[k] != '0' (B has no leading zero)
    #   # 2. int(S[:k]) >= int(S[k:])
    #   # Since numbers can be huge, we compare lengths first.
    #   # If len(A) > len(B), then A > B always.
    #   # If len(A) < len(B), then A < B always.
    #   # If len(A) == len(B), compare lexicographically.
    #   
    #   # Optimization:
    #   # We iterate k from 1 upwards.
    #   # len(A) = L - k, len(B) = k.
    #   # Condition len(A) > len(B) => L - k > k => 2k < L => k < L/2.
    #   # If we find any k < L/2 such that S[k] != '0', then A > B is guaranteed.
    #   # So the first k (smallest) with S[k] != '0' and k < L/2 is a candidate.
    #   # If no such k exists (i.e., all k < L/2 have S[k] == '0'), we check k >= L/2.
    #   # For k >= L/2, len(A) <= len(B).
    #   # We need explicit comparison.
    #   
    #   # Actually, we just need the smallest k.
    #   # Iterate k from 1 to L-1.
    #   # Check if S[k] != '0'.
    #   # If so, check value condition.
    #   # If valid, we take this split, update S = S[:k], count++, break loop (greedy).
    #   
    #   # Wait, is it always optimal to take the smallest k?
    #   # Suppose S = "1001".
    #   # k=1: S[1]='0' skip.
    #   # k=2: S[2]='0' skip.
    #   # k=3: S[3]='1'. B="1". A="100". 100 >= 1. Valid.
    #   # Split -> "100".
    #   # Now S="100".
    #   # k=1: '0' skip.
    #   # k=2: '0' skip.
    #   # No valid split. Stop.
    #   # Total count = 1 (initial) + 1 (split) = 2.
    #   # Original: {100, 1} -> {1001}.
    #   # Could we have done better?
    #   # Maybe split differently? No, we must split from the end in reverse.
    #   # The reverse process is deterministic in structure: we peel off a suffix.
    #   # The only choice is which suffix.
    #   # Peeling a shorter suffix leaves a longer prefix, which is better for future splits.
    #   # So yes, greedy smallest k is optimal.
    #
    # Implementation details:
    # S is a string.
    # Loop while len(S) > 1:
    #   best_k = -1
    #   L = len(S)
    #   for k in range(1, L):
    #     if S[k] == '0': continue
    #     A = S[:k]
    #     B = S[k:]
    #     # Compare A and B
    #     if len(A) > len(B):
    #       valid = True
    #     elif len(A) < len(B):
    #       valid = False
    #     else:
    #       valid = (A >= B) # lexicographical compare works for same length strings of digits
    #     
    #     if valid:
    #       best_k = k
    #       break # Found smallest k
    #   
    #   if best_k == -1:
    #     break # Cannot split anymore
    #   
    #   S = S[:best_k]
    #   count += 1
    #
    # Print count.

    count = 1
    while True:
        L = len(s)
        if L <= 1:
            break
        
        best_k = -1
        # Optimization: 
        # If there is any k < L/2 with s[k] != '0', that is the best candidate because len(A) > len(B).
        # We just need the first such k.
        # If not, we have to check k >= L/2.
        
        # Check for k < L/2
        limit = L // 2
        found_short = -1
        for k in range(1, limit + 1):
            if s[k] != '0':
                found_short = k
                break
        
        if found_short != -1:
            best_k = found_short
        else:
            # Check k >= L/2
            # We need to iterate from limit+1 to L-1
            # But we want the smallest k, so start from limit+1
            for k in range(limit + 1, L):
                if s[k] == '0':
                    continue
                # Compare s[:k] and s[k:]
                # Since len(A) <= len(B), we need explicit check
                # A = s[:k], B = s[k:]
                # If len(A) < len(B), A < B -> invalid
                # If len(A) == len(B), check lexicographically
                if k > L - k: # len(A) < len(B)
                    continue
                # len(A) <= len(B)
                # If len(A) < len(B), then A < B (since no leading zeros, shorter is smaller)
                # Wait, is it possible for shorter to be larger? No, positive integers.
                # So if len(A) < len(B), invalid.
                if k < L - k:
                    continue
                # len(A) == len(B)
                if s[:k] >= s[k:]:
                    best_k = k
                    break
        
        if best_k == -1:
            break
        
        s = s[:best_k]
        count += 1
        
    print(count)

if __name__ == '__main__':
    solve()