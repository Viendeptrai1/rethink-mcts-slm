def is_nested(string):
    # We need to find if there exists a valid subsequence of brackets that has at least one nesting.
    # A valid bracket sequence is one where every opening bracket has a matching closing bracket
    # and they are properly nested.
    # A sequence has nesting if there is at least one pair of brackets (i, j) such that i < j,
    # bracket[i] == '[', bracket[j] == ']', and there is at least one bracket between them that is part of the valid subsequence.
    # Actually, simpler: a valid sequence has nesting if it is not just a concatenation of disjoint [] pairs.
    # But we are looking for a SUBSEQUENCE.
    
    # Key Insight:
    # If we can find a valid subsequence that contains a pattern like "[...]" where the "..." is non-empty and valid, then it's nested.
    # Actually, the simplest way to have nesting in a valid subsequence is to have a structure like "[A]" where A is a non-empty valid sequence.
    # Or more generally, if we have a valid subsequence that is not just a sequence of "[]" concatenated.
    
    # However, note the examples:
    # '[]]]]]]][[[[[]' -> False. 
    # Let's try to form a valid subsequence. We can pick indices.
    # The string has many closing brackets then opening. 
    # To form a valid sequence, we need matching pairs.
    # The only valid subsequence we can form might be "[]" (from the last two characters? no, last two are '][').
    # Actually, let's look at the string: '[]]]]]]][[[[[]'
    # Indices: 0: '[', 1: ']', 2: ']', ... 8: ']', 9: '[', 10: '[', 11: '[', 12: '[', 13: ']'
    # We can pick index 0 and 1 to get "[]". No nesting.
    # Can we pick more? 
    # If we pick index 9, 10, 11, 12, 13 -> "[[[[ ]" -> invalid.
    # We need to match. 
    # Maybe index 0, 1, 9, 13? -> "[] [ ]" -> valid but no nesting (it's two disjoint pairs).
    # To have nesting, we need something like "[ [ ] ]" or "[ [ [ ] ] ]".
    # This requires at least 4 brackets in the subsequence: outer pair and inner pair.
    # So if the length of the longest valid subsequence is less than 4, it can't be nested? 
    # Not necessarily: "[][]" has length 4 but no nesting. "[[]]" has length 4 and has nesting.
    # So we need to check if there is a valid subsequence that is NOT just a concatenation of "[]" pairs.
    
    # Alternative approach:
    # A valid subsequence has nesting if and only if there exists a valid subsequence that contains a substring (in the subsequence) of the form "[...]" where the "..." is a non-empty valid sequence.
    # This is equivalent to saying the valid subsequence is not a sequence of disjoint "[]" pairs.
    
    # How about this: 
    # If we can find two pairs of brackets (i, j) and (k, l) such that i < k < j < l, then we can form a nested structure?
    # Not exactly. We need the subsequence to be valid.
    
    # Let's reframe:
    # We want to know if there is a valid subsequence S such that S is not of the form "[]" repeated k times.
    # Actually, any valid sequence that is not a concatenation of "[]" must have some nesting.
    # Proof: If a valid sequence has no nesting, then every opening bracket must be immediately followed by its closing bracket in the subsequence? 
    # No, consider "[] []". This has no nesting. But "[] [ ]" is two separate pairs.
    # In "[] []", the first pair is at indices 0,1 and second at 2,3. They are disjoint.
    # In "[[]]", the inner pair is at 1,2 and outer at 0,3. They are nested.
    
    # So the condition is: does there exist a valid subsequence that is not a concatenation of disjoint "[]" pairs?
    # This is equivalent to: does there exist a valid subsequence that has a pair of brackets (i, j) in the subsequence such that there is another pair (k, l) in the subsequence with i < k < j < l? 
    # No, that's not the definition of nesting. Nesting is i < k < l < j.
    # Yes: nesting means one pair is inside another. So i < k < l < j.
    
    # So we need to find if there exist indices i < k < l < j in the original string such that:
    # string[i] == '[', string[j] == ']', string[k] == '[', string[l] == ']'
    # AND the subsequence formed by indices i, k, l, j is valid.
    # The subsequence is "[ [ ] ]", which is valid.
    # So if we can find such indices, then we have a nested valid subsequence.
    
    # But wait, what if the subsequence is longer? 
    # If we have a valid subsequence with nesting, it must contain at least one pair of nested brackets.
    # So if there is any valid subsequence with nesting, then there must be indices i < k < l < j such that 
    # string[i] == '[', string[j] == ']', string[k] == '[', string[l] == ']'
    # and the subsequence restricted to these four indices is "[ [ ] ]", which is valid.
    # Therefore, the condition simplifies to: 
    # Does there exist i < k < l < j such that string[i] == '[', string[k] == '[', string[l] == ']', string[j] == ']'?
    # If yes, then we can form the subsequence "[ [ ] ]" which is valid and nested.
    # If no, then no such nested structure exists.
    
    # Let's test with examples:
    # '[[]]': i=0, k=1, l=2, j=3 -> '[', '[', ']', ']' -> yes.
    # '[][]': 
    #   i=0, k=2, l=3, j=? -> no j after 3.
    #   i=0, k=1, l=3, j=? -> no j after 3.
    #   Actually, we need i < k < l < j.
    #   In '[][]', we have indices 0,1,2,3.
    #   Possible i,k,l,j: 
    #     i=0 ('['), k=1 (']') -> not '['.
    #     i=0 ('['), k=2 ('['), l=3 (']') -> need j>3, none.
    #   So no such quadruple. -> False. Correct.
    # '[]]]]]]][[[[[]':
    #   We need i < k < l < j with '[', '[', ']', ']'.
    #   The string has '[' at 0, then many ']', then '[' at 9,10,11,12, then ']' at 13.
    #   We need two '[' before two ']'.
    #   The '[' are at 0, 9, 10, 11, 12.
    #   The ']' are at 1, 2, 3, 4, 5, 6, 7, 8, 13.
    #   We need i < k < l < j.
    #   Try i=0, k=9. Then we need l and j such that 9 < l < j and string[l]=']', string[j]=']'.
    #   We have l=13, but we need j>13, none.
    #   Try i=0, k=10. Then l=13, j>13 none.
    #   Try i=9, k=10. Then l=13, j>13 none.
    #   So no such quadruple. -> False. Correct.
    # '[[][]]':
    #   i=0, k=1, l=2, j=5? 
    #   string[0]='[', string[1]='[', string[2]=']', string[5]=']'.
    #   Indices: 0 < 1 < 2 < 5. Yes. -> True. Correct.
    # '[[]][[':
    #   i=0, k=1, l=2, j=3? 
    #   string[0]='[', string[1]='[', string[2]=']', string[3]=']'.
    #   Indices: 0 < 1 < 2 < 3. Yes. -> True. Correct.
    
    # So the algorithm is:
    # Find if there exist indices i < k < l < j such that:
    # string[i] == '[', string[k] == '[', string[l] == ']', string[j] == ']'
    
    # We can do this by:
    # 1. Find the first occurrence of '[' -> i
    # 2. Find the first occurrence of '[' after i -> k
    # 3. Find the first occurrence of ']' after k -> l
    # 4. Find the first occurrence of ']' after l -> j
    # If all exist, return True.
    
    # But wait, what if the first '[' is not the best i?
    # Actually, if there is ANY such quadruple, then the first '[' (smallest i) will work for i, 
    # and then we need k > i, l > k, j > l.
    # If we take the smallest i, then we have the most room for k, l, j.
    # Similarly, for k, we want the smallest k > i to leave room for l and j.
    # Then smallest l > k, then smallest j > l.
    # So greedy approach works.
    
    n = len(string)
    i = -1
    # Find first '['
    for idx in range(n):
        if string[idx] == '[':
            i = idx
            break
    if i == -1:
        return False
    
    k = -1
    # Find first '[' after i
    for idx in range(i + 1, n):
        if string[idx] == '[':
            k = idx
            break
    if k == -1:
        return False
    
    l = -1
    # Find first ']' after k
    for idx in range(k + 1, n):
        if string[idx] == ']':
            l = idx
            break
    if l == -1:
        return False
    
    j = -1
    # Find first ']' after l
    for idx in range(l + 1, n):
        if string[idx] == ']':
            j = idx
            break
    if j == -1:
        return False
    
    return True