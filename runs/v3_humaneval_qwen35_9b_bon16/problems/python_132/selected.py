def is_nested(string):
    """
    Create a function that takes a string as input which contains only square brackets.
    The function should return True if and only if there is a valid subsequence of brackets 
    where at least one bracket in the subsequence is nested.
    """
    # We need to find if there exists a valid subsequence that contains nesting.
    # A nested structure like "[[]]" requires a ']' that closes an opening bracket
    # which was itself opened after a previous closing bracket or at the start.
    # Actually, let's re-evaluate the condition.
    # A valid bracket sequence is nested if it has the form [A] where A is not empty.
    # We can form such a subsequence if we can find an index i and j (i < j) such that:
    # 1. s[i] == '['
    # 2. s[j] == ']'
    # 3. There exists a valid non-empty bracket subsequence between i and j (exclusive) that can close s[i] and open s[j]?
    # Wait, the problem asks for a valid subsequence that is nested.
    # A simple nested sequence is "[]". But "[]" is not nested in the sense of having a bracket inside another.
    # The example "[[]]" is True. The subsequence is the whole string.
    # The example "[][]" is False. The subsequences are "[]", "[]", "[[]]" (taking indices 0,1,2,3? No, subsequence keeps order).
    # If we take indices 0, 2, 3 from "[][]" -> "[[]" not valid.
    # If we take indices 0, 1, 2, 3 -> "[][]" not nested.
    # If we take indices 0, 2 -> "[]" not nested.
    # So we need to find if there is a subsequence that forms a valid bracket sequence AND has at least one pair nested.
    # A valid bracket sequence is nested if it is not just a concatenation of disjoint valid sequences like "[] []".
    # It must look like [ ... ] where the inside is non-empty and valid.
    # So we need to find indices i < k < j such that s[i] = '[', s[j] = ']', and there is a valid subsequence inside (i, j) that is non-empty.
    # Actually, the simplest nested structure is "[[]]".
    # This requires:
    # 1. An opening bracket at index i.
    # 2. A closing bracket at index j (j > i).
    # 3. At least one opening bracket at index k (i < k < j).
    # 4. At least one closing bracket at index m (k < m < j).
    # 5. The subsequence s[i], s[k], s[m], s[j] must be valid. Since it is "[[]]", it is valid.
    # So the condition simplifies to: Can we find indices i < k < m < j such that s[i] = '[', s[k] = '[', s[m] = ']', s[j] = ']'?
    # If we have "[[]]", indices 0, 1, 2, 3 work.
    # If we have "[[][]]", we can pick 0, 1, 2, 4 -> "[[]]" valid nested.
    # If we have "[[]][[" (from example), we can pick 0, 1, 2, 3 -> "[[]]" valid nested.
    # What about "[][]"? 
    # Indices: 0:[, 1:], 2:[, 3:].
    # We need i < k < m < j with [ [ ] ].
    # Possible i=0. Need k, m, j in (0, 3).
    # Available: 1:], 2:[, 3:].
    # Can we pick k=2 ([), m=1 (])? No, m must be > k.
    # So we need two '[' and two ']' such that the first '[' comes before the second '[' and the second ']' comes after the second '['?
    # No, the structure is [ [ ] ].
    # Order: '[' (outer), '[' (inner), ']' (inner), ']' (outer).
    # So we need index of first '[' < index of second '[' < index of first ']' < index of second ']'.
    # Let's check "[][]":
    # [ at 0, ] at 1, [ at 2, ] at 3.
    # Can we find i < k < m < j such that s[i]='[', s[k]='[', s[m]=']', s[j]=']'?
    # i must be 0 or 2? If i=0, then k must be 2. Then m must be > 2, so m=3. Then j must be > 3. None.
    # If i=2, k must be > 2. No other '['.
    # So "[][]" is False. Correct.
    # Check "[[]]": 0, 1, 2, 3. i=0, k=1, m=2, j=3. Valid.
    # Check "[]]]]]]][[[[[]":
    # We need i < k < m < j.
    # Count of '[' before some index and count of ']' after some index?
    # We just need to find if there exist 4 indices i < k < m < j with pattern [ [ ] ].
    # This is equivalent to finding if the string contains a subsequence "[[]]".
    # Algorithm:
    # Find the first '['. Let it be i.
    # Find the first '[' after i. Let it be k.
    # Find the first ']' after k. Let it be m.
    # Find the first ']' after m. Let it be j.
    # If all exist, return True.
    # Is it possible that a different selection works but the greedy one fails?
    # We want ANY valid subsequence.
    # If there is a valid [ [ ] ] subsequence, then there exists i1 < k1 < m1 < j1 with the pattern.
    # To maximize our chances of finding the next character, we should pick the earliest possible indices.
    # So:
    # 1. Find first '[' -> i.
    # 2. Find first '[' after i -> k.
    # 3. Find first ']' after k -> m.
    # 4. Find first ']' after m -> j.
    # If we find all, then True.
    # Is it possible that we need to skip the first '[' to find a solution?
    # Suppose the string is "][[[]]".
    # Greedy: first '[' is at 1. Next '[' at 2. Next ']' at 3. Next ']' at 4. Found.
    # Suppose string is "[ [ ] ]". Found.
    # Suppose string is "[ [ ] [ ] ]".
    # Greedy: 0, 1, 2, 3 -> "[[]]". Found.
    # Is there a case where greedy fails but solution exists?
    # We need i < k < m < j.
    # If a solution exists, let the indices be a < b < c < d.
    # i (first '[') <= a.
    # k (first '[' after i) <= b (since b is a '[' after a, and i <= a, so b is after i. Since k is the FIRST after i, k <= b).
    # m (first ']' after k) <= c (since c is a ']' after b, and k <= b, so c is after k. Since m is FIRST after k, m <= c).
    # j (first ']' after m) <= d (similar logic).
    # So if a solution exists, the greedy approach will also find indices i', k', m', j' satisfying the order.
    # Thus, the greedy strategy is sufficient.

    def find_char_after(target, start_idx):
        for idx in range(start_idx, len(string)):
            if string[idx] == target:
                return idx
        return -1

    # Find first '['
    i = find_char_after('[', 0)
    if i == -1:
        return False
    
    # Find second '[' after i
    k = find_char_after('[', i + 1)
    if k == -1:
        return False
        
    # Find first ']' after k
    m = find_char_after(']', k + 1)
    if m == -1:
        return False
        
    # Find second ']' after m
    j = find_char_after(']', m + 1)
    if j == -1:
        return False
        
    return True