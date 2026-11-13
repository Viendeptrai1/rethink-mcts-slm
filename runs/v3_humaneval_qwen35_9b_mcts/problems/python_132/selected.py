def is_nested(string):
    n = len(string)
    if n < 4:
        return False

    # dp[i][j] = length of the longest valid bracket subsequence in s[i:j+1]
    # has_nested[i][j] = True if that subsequence contains at least one nesting
    dp = [[0] * n for _ in range(n)]
    has_nested = [[False] * n for _ in range(n)]

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if string[i] == '[' and string[j] == ']':
                # Check if the inner part is valid
                inner_len = j - i - 1
                if inner_len == 0:
                    # "[]" -> valid, no nesting
                    dp[i][j] = 2
                    has_nested[i][j] = False
                else:
                    # Try to match i and j with a valid inner sequence
                    # We need dp[i+1][j-1] > 0
                    if dp[i+1][j-1] > 0:
                        dp[i][j] = 2 + dp[i+1][j-1]
                        # Nesting occurs if the inner part itself has nesting OR
                        # if the inner part is non-empty (which it is) and we are forming a pair around it.
                        # Actually, the definition of nesting is having a bracket inside another.
                        # If we have "[]", no nesting.
                        # If we have "[[]]", we have nesting.
                        # So if inner_len > 0 and we successfully matched i and j, we have nesting.
                        has_nested[i][j] = True
                    else:
                        # Cannot form a pair with i and j directly enclosing a valid sequence
                        dp[i][j] = 0
                        has_nested[i][j] = False

            # Also consider splitting the range [i, j] into two parts
            for k in range(i, j):
                if dp[i][k] > 0 and dp[k+1][j] > 0:
                    current_len = dp[i][k] + dp[k+1][j]
                    if current_len > dp[i][j]:
                        dp[i][j] = current_len
                        has_nested[i][j] = has_nested[i][k] or has_nested[k+1][j]

    # Check if the entire string has a valid subsequence with nesting
    # We need to find if there exists any subsequence that is valid and has nesting.
    # Our DP above computes the longest valid subsequence for every substring.
    # However, the problem asks for a subsequence, not a substring.
    # The standard DP for longest valid parentheses works on substrings.
    # To handle subsequences, we need a different approach.

    # Let's reconsider. We need to select a subsequence of brackets that forms a valid sequence
    # and has at least one nesting.
    # A valid bracket sequence is defined by matching pairs.
    # Nesting means we have a pair (i, j) and another pair (k, l) such that i < k < l < j.

    # Since we can pick any subsequence, we can think of this as:
    # Can we form a valid sequence of length >= 4 that has nesting?
    # The smallest valid sequence with nesting is "[[]]" (length 4).
    # So we just need to check if we can form "[[]]" as a subsequence.
    # Wait, is that true?
    # Example: '[]]]]]]][[[[[]' -> False.
    # Subsequences: "[]", "[[]", etc.
    # Can we form "[[]]"?
    # Indices: 0,1,2,3...
    # s[0]='[', s[1]=']', s[2]=']', ...
    # To form "[[]]", we need two '[' and two ']' such that the structure is nested.
    # Structure: [ ... [ ... ] ... ]
    # So we need index i < k < l < j such that s[i]='[', s[k]='[', s[l]=']', s[j]=']'.
    # This is exactly checking if the subsequence "[[]]" exists.

    # Let's verify with examples.
    # '[[]]' -> indices 0,1,2,3. i=0, k=1, l=2, j=3. Yes.
    # '[][]' -> indices 0,1,2,3. s[0]='[', s[1]=']', s[2]='[', s[3]=']'.
    # Can we pick i<k<l<j?
    # i=0 ('['), k=2 ('['), l=3 (']'), j=? No j > 3.
    # i=0, k=1? s[1]=']' not '['.
    # So '[][]' does not contain "[[]]" as a subsequence. Correct.
    # '[]' -> length 2, cannot form length 4. Correct.
    # '[[][]]' -> indices 0,1,2,3,4,5.
    # i=0 ('['), k=2 ('['), l=3 (']'), j=5 (']'). Yes.
    # '[[]][[' -> indices 0,1,2,3,4,5.
    # i=0 ('['), k=1 ('['), l=2 (']'), j=3 (']'). Yes.

    # So the problem reduces to: Does the string contain the subsequence "[[]]"?
    # We need to find indices i < k < l < j such that s[i] == '[', s[k] == '[', s[l] == ']', s[j] == ']'.

    # Algorithm:
    # 1. Find the first '['. Let this be i.
    # 2. Find the first '[' after i. Let this be k.
    # 3. Find the first ']' after k. Let this be l.
    # 4. Find the first ']' after l. Let this be j.
    # If all found, return True.

    # Wait, is it always the first ones?
    # Suppose s = "[ [ ] ] ] ]".
    # i=0, k=1, l=2, j=3. Works.
    # What if s = "[ ] [ ] ] ]"?
    # i=0, k=2, l=3, j=4. Works.
    # What if s = "[ [ [ ] ] ]"?
    # i=0, k=1, l=3, j=4. Works.

    # Is it possible that picking the first available doesn't work but a later one does?
    # We need i < k < l < j.
    # To maximize the chance of finding l and j, we should minimize i and k.
    # So picking the first available i and k is optimal.
    # Similarly, to maximize the chance of finding j, we should minimize l.
    # So picking the first available l after k is optimal.
    # Therefore, the greedy approach works.

    # Let's re-verify the logic.
    # We need to find 4 indices i < k < l < j with pattern [ [ ] ].
    # Greedy:
    # i = first index of '['
    # k = first index of '[' after i
    # l = first index of ']' after k
    # j = first index of ']' after l
    # If all exist, return True, else False.

    # Example 2: '[]]]]]]][[[[[]'
    # i = 0 ('[')
    # k = ? Next '[' after 0.
    # s[0]='[', s[1]=']', s[2]=']', s[3]=']', s[4]=']', s[5]=']', s[6]=']', s[7]=']', s[8]='[', ...
    # k = 8
    # l = first ']' after 8.
    # s[9]='[', s[10]='[', s[11]='[', s[12]='[', s[13]=']'.
    # l = 13
    # j = first ']' after 13. None.
    # Returns False. Correct.

    # Example: '[][]'
    # i = 0
    # k = 2
    # l = 3
    # j = ? None.
    # Returns False. Correct.

    # Example: '[[][]]'
    # i = 0
    # k = 2
    # l = 3
    # j = 5
    # Returns True. Correct.

    # Example: '[[]][['
    # i = 0
    # k = 1
    # l = 2
    # j = 3
    # Returns True. Correct.

    # One edge case: what if the string is "[[][]" (missing last ])?
    # i=0, k=2, l=3, j=? None. False. Correct.

    # What if string is "[][][]"?
    # i=0, k=2, l=3, j=5. True.
    # Is there a valid nested subsequence? Yes, indices 0,2,3,5 form "[[]]".
    # Wait, s[0]='[', s[2]='[', s[3]=']', s[5]=']'.
    # Subsequence: s[0], s[2], s[3], s[5] -> "[[]]". Valid and nested. Correct.

    # So the solution is simply to check for the subsequence "[[]]".

    i = -1
    # Find first '['
    for idx, char in enumerate(string):
        if char == '[':
            i = idx
            break
    if i == -1:
        return False

    k = -1
    # Find first '[' after i
    for idx in range(i + 1, len(string)):
        if string[idx] == '[':
            k = idx
            break
    if k == -1:
        return False

    l = -1
    # Find first ']' after k
    for idx in range(k + 1, len(string)):
        if string[idx] == ']':
            l = idx
            break
    if l == -1:
        return False

    j = -1
    # Find first ']' after l
    for idx in range(l + 1, len(string)):
        if string[idx] == ']':
            j = idx
            break
    if j == -1:
        return False

    return True