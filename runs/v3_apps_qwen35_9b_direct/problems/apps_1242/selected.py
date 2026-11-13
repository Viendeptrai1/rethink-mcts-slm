import sys

def solve():
    s = sys.stdin.readline().strip()
    n = len(s)
    res = [0] * n
    
    # We simulate the process from i = 0 to n-1 (prefix lengths 1 to n)
    # At each step i, we decide whether to reverse the prefix s[0...i].
    # The decision is greedy: we want the character at position i to be as small as possible ('a').
    # If the current character at i is 'b', we reverse the prefix to make it 'a' (since reversing swaps s[i] with s[0], and if s[0] was 'a', it becomes 'a' at i).
    # If the current character at i is already 'a', we do nothing to keep it 'a'.
    # Note: Reversing a prefix changes the order of characters within that prefix, but the multiset of characters in the prefix remains the same.
    # However, the key observation is that at step i, we only care about the character at index i.
    # By maintaining the current state of the string, we can check s[i].
    
    current_s = list(s)
    
    for i in range(n):
        if current_s[i] == 'b':
            # We need to make this 'a'.
            # Reversing the prefix s[0...i] will swap current_s[i] with current_s[0].
            # Since we are processing left to right and making decisions greedily for lexicographical minimality,
            # it turns out that if we encounter a 'b' at position i, reversing the prefix is the optimal move
            # to potentially bring an 'a' to this position (assuming the prefix contains an 'a', which it must if we are to improve).
            # Actually, the logic is simpler: if current_s[i] is 'b', we reverse. If it is 'a', we don't.
            # Why? Because if we have a 'b' at i, and we don't reverse, it stays 'b'. If we reverse, the new char at i becomes the old char at 0.
            # But wait, the problem says we consider prefixes in order. The state of the string evolves.
            # Let's trace:
            # If current_s[i] == 'b', we reverse prefix 0..i. This sets res[i] = 1.
            # If current_s[i] == 'a', we leave it, res[i] = 0.
            # Is this correct?
            # Example 1: bbab
            # i=0: s[0]='b'. Reverse prefix 0..0? Reversing a single char does nothing. But the example output says 0 1 1 0.
            # Let's re-read the example note.
            # "IA can reverse the second and the third prefix and get a string 'abbb'."
            # Initial: b b a b
            # Prefix 1 (len 1): "b" -> reverse -> "b". String: b b a b.
            # Prefix 2 (len 2): "bb" -> reverse -> "bb". String: b b a b.
            # Prefix 3 (len 3): "bba" -> reverse -> "abb". String: a b b b.
            # Prefix 4 (len 4): "abbb" -> reverse -> "bbba". String: b b b a.
            # Wait, the example output is 0 1 1 0.
            # Let's trace 0 1 1 0 on "bbab":
            # i=0 (len 1): res[0]=0. No reverse. S: b b a b
            # i=1 (len 2): res[1]=1. Reverse s[0:2] ("bb" -> "bb"). S: b b a b
            # i=2 (len 3): res[2]=1. Reverse s[0:3] ("bba" -> "abb"). S: a b b b
            # i=3 (len 4): res[3]=0. No reverse. S: a b b b
            # Result: "abbb". This matches the note.
            
            # So the logic is:
            # At step i, look at the current character at index i.
            # If it is 'b', we MUST reverse the prefix to try to get an 'a' there?
            # In the example above, at i=1, s[1] was 'b'. We reversed. s[0] was 'b', s[1] was 'b'. Reversing did nothing to the value at index 1, but it set up the string for the next step.
            # At i=2, s[2] was 'a'. We reversed. s[0] was 'b', s[1] was 'b', s[2] was 'a'. Reversing "bba" -> "abb". Now s[2] is 'b'.
            # Wait, if s[2] was 'a', why reverse? The goal is lexicographically smallest.
            # If we don't reverse at i=2, s[2] stays 'a'. If we reverse, s[2] becomes 'b'. 'a' < 'b', so we should NOT reverse if s[i] is 'a'.
            # But the example output says reverse at i=2 (index 2, 3rd prefix).
            # Let's re-examine the example trace carefully.
            # Initial: b b a b
            # Step 1 (i=0): Prefix "b". Options: "b" or "b". Best is "b". No reverse. S: b b a b.
            # Step 2 (i=1): Prefix "bb". Options: "bb" or "bb". Best is "bb". No reverse?
            # But the example output has 1 at index 1.
            # Maybe the greedy strategy isn't just "if s[i] == 'b' then reverse".
            # Let's look at the result "abbb".
            # How do we get 'a' at index 0?
            # The only way to get 'a' at index 0 is if at some step k >= 0, we reverse a prefix that includes the 'a' and moves it to 0.
            # The 'a' is initially at index 2.
            # To move 'a' from index 2 to index 0, we must reverse a prefix of length >= 3.
            # Specifically, if we reverse prefix of length 3 ("bba" -> "abb"), the 'a' moves to index 1.
            # If we then reverse prefix of length 4? No, we process in order.
            # Let's re-simulate the example output 0 1 1 0 step by step with the actual string updates.
            # Start: s = ['b', 'b', 'a', 'b']
            # i=0: res[0]=0. Prefix len 1: s[0:1] = "b". Reverse? No. s remains ['b', 'b', 'a', 'b'].
            # i=1: res[1]=1. Prefix len 2: s[0:2] = "bb". Reverse -> "bb". s remains ['b', 'b', 'a', 'b'].
            # i=2: res[2]=1. Prefix len 3: s[0:3] = "bba". Reverse -> "abb". s becomes ['a', 'b', 'b', 'b'].
            # i=3: res[3]=0. Prefix len 4: s[0:4] = "abbb". Reverse? No. s remains ['a', 'b', 'b', 'b'].
            # Final: "abbb".
            
            # Why did we reverse at i=1 and i=2?
            # At i=1, s[1] was 'b'. If we didn't reverse, s[1] stays 'b'. If we reverse, s[1] stays 'b' (since s[0]==s[1]).
            # At i=2, s[2] was 'a'. If we didn't reverse, s[2] stays 'a'. If we reverse, s[2] becomes 'b'.
            # This seems counter-intuitive. Why reverse if it makes the current position worse ('a' -> 'b')?
            # Ah, because reversing changes the ENTIRE prefix. It might set up a better configuration for future steps.
            # Specifically, reversing at i=2 moved the 'a' from index 2 to index 0.
            # Once 'a' is at index 0, the string starts with 'a', which is the best possible start.
            # If we didn't reverse at i=2, the string would be "bba..." which starts with 'b'.
            # "a..." is lexicographically smaller than "b...".
            # So the decision at step i depends on whether reversing the prefix helps us get a smaller character at index 0 eventually?
            # Actually, the standard solution for this problem (Codeforces 1141B? No, this is likely "IA and Magnets" or similar) is:
            # Iterate i from 0 to n-1.
            # If s[i] == 'b', reverse the prefix s[0...i].
            # If s[i] == 'a', do not reverse.
            # Let's test this hypothesis on "bbab".
            # i=0: s[0]='b'. Reverse prefix 0..0. s="bbab". res[0]=1.
            # i=1: s[1]='b'. Reverse prefix 0..1 ("bb"->"bb"). s="bbab". res[1]=1.
            # i=2: s[2]='a'. Do not reverse. s="bbab". res[2]=0.
            # i=3: s[3]='b'. Reverse prefix 0..3 ("bbab"->"babb"). s="babb". res[3]=1.
            # Result: 1 1 0 1. String "babb".
            # Is "babb" < "abbb"? No. "abbb" is smaller.
            # So the hypothesis "if s[i]=='b' reverse" is WRONG.
            
            # Let's try the reverse logic:
            # If s[i] == 'a', reverse?
            # i=0: s[0]='b'. No.
            # i=1: s[1]='b'. No.
            # i=2: s[2]='a'. Yes. Reverse "bba" -> "abb". s="abbb".
            # i=3: s[3]='b'. No.
            # Result: 0 0 1 0. String "abbb".
            # This matches the final string "abbb".
            # But the example output is 0 1 1 0.
            # Both 0 0 1 0 and 0 1 1 0 yield "abbb".
            # The problem says: "If there are multiple possible sequences leading to the optimal answer, print any of them."
            # So 0 0 1 0 is a valid answer.
            # Let's check the second example: "aaaaa".
            # Logic: if s[i] == 'a', reverse.
            # i=0: 'a' -> reverse. s="aaaaa".
            # i=1: 'a' -> reverse. s="aaaaa".
            # ...
            # Result: 1 1 1 1 1.
            # Example output: 1 0 0 0 1.
            # Both yield "aaaaa". Valid.
            
            # So the strategy seems to be:
            # If the current character at i is 'a', we reverse the prefix.
            # If the current character at i is 'b', we do not reverse.
            # Why?
            # If s[i] is 'a', reversing the prefix s[0...i] will move s[0] to s[i] and s[i] to s[0].
            # Since s[i] is 'a', after reversal, s[0] becomes 'a'.
            # Having 'a' at the beginning of the string is always better for lexicographical order.
            # If s[i] is 'b', reversing would put s[0] (whatever it is) at s[i], and 'b' at s[0].
            # If s[0] was 'a', then after reversal s[0] becomes 'b', which is bad.
            # If s[0] was 'b', then after reversal s[0] stays 'b', no improvement at start, and we might mess up the rest.
            # So the rule: Reverse if and only if s[i] == 'a'.
            
            # Let's verify with "bbab" again.
            # s = b b a b
            # i=0: s[0]='b'. No reverse. res[0]=0. s: b b a b
            # i=1: s[1]='b'. No reverse. res[1]=0. s: b b a b
            # i=2: s[2]='a'. Reverse. res[2]=1. s[0:3] "bba" -> "abb". s: a b b b
            # i=3: s[3]='b'. No reverse. res[3]=0. s: a b b b
            # Output: 0 0 1 0. Valid.
            
            # Let's try another case. "ba".
            # i=0: s[0]='b'. No. s: b a
            # i=1: s[1]='a'. Yes. Reverse "ba" -> "ab". s: a b
            # Output: 0 1. Result "ab". Correct.
            
            # Case "ab".
            # i=0: s[0]='a'. Yes. Reverse "a" -> "a". s: a b
            # i=1: s[1]='b'. No. s: a b
            # Output: 1 0. Result "ab". Correct.
            
            # Case "b".
            # i=0: s[0]='b'. No.
            # Output: 0. Result "b". Correct.
            
            # Case "a".
            # i=0: s[0]='a'. Yes.
            # Output: 1. Result "a". Correct.
            
            # The logic holds.
            # Algorithm:
            # 1. Read string s.
            # 2. Convert to list for mutability.
            # 3. Initialize res array of 0s.
            # 4. Loop i from 0 to n-1:
            #    If s[i] == 'a':
            #       Reverse s[0...i]
            #       res[i] = 1
            #    Else:
            #       res[i] = 0
            # 5. Print res.
            
            # Wait, reversing a list slice in Python is O(k). Total time O(n^2).
            # Given n <= 1000, n^2 = 1,000,000, which is well within time limits (usually 1-2 seconds for ~10^8 ops).
            # So simulation is fine.
            
            pass # Logic confirmed

    # Implementation
    current_s = list(s)
    res = []
    
    for i in range(n):
        if current_s[i] == 'a':
            # Reverse prefix 0 to i
            current_s[:i+1] = current_s[:i+1][::-1]
            res.append(1)
        else:
            res.append(0)
            
    print(*(res))

if __name__ == '__main__':
    solve()