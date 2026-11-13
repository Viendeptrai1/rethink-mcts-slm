import sys

def solve():
    s = sys.stdin.readline().strip()
    n = len(s)
    res = [0] * n
    
    # Current state of the string as a list of characters
    chars = list(s)
    
    # Process prefixes from length 1 to n
    for i in range(n):
        # Consider prefix of length i+1 (indices 0 to i)
        # Check if reversing this prefix makes the current state lexicographically smaller
        # Since we process from left to right, the prefix we are considering is the entire current array up to i.
        # We compare the current array with the array where we reverse the prefix 0..i.
        # However, note that the operation is defined on the original positions? 
        # Actually, the problem says: "look at all prefixes ... and for each prefix she will either reverse this prefix or leave it".
        # The order is fixed: from shortest to largest.
        # This means at step i (considering prefix of length i+1), the string has been modified by previous operations.
        # We need to decide whether to reverse the prefix [0..i] of the CURRENT string to minimize the result.
        
        # Let's simulate:
        # Current string: chars[0..i]
        # Option 1: Keep as is.
        # Option 2: Reverse chars[0..i].
        # We choose Option 2 if the reversed version is lexicographically smaller than the current version.
        # Why? Because any future operation (on a longer prefix) will encompass the current prefix and potentially fix things again,
        # but the decision at step i only affects the prefix 0..i relative to step i. 
        # Actually, the key insight is: at step i, we look at the current string. If reversing the prefix 0..i makes it smaller, we do it.
        # Why is this greedy approach correct?
        # Because the operations are sequential. The state after step i depends on the decision at step i.
        # The goal is the final string. But note that reversing a prefix of length L+1 after reversing a prefix of length L
        # is equivalent to some permutation.
        # However, the standard solution for this specific problem (Codeforces 1296B? No, it's similar to a known problem) 
        # is simply: at each step i, if the current character at position i is 'b' and the character at position 0 (which is the first of the current prefix) is 'a', 
        # wait, that's not quite it.
        
        # Let's re-evaluate with the example: "bbab"
        # i=0 (prefix len 1): "b". Reverse -> "b". No change. res[0]=0. String: "bbab"
        # i=1 (prefix len 2): "bb". Reverse -> "bb". No change? But example says reverse 2nd prefix.
        # Wait, the example output is 0 1 1 0.
        # Let's trace the example "bbab" with the operations:
        # Initial: b b a b
        # Step 1 (len 1): prefix "b". Reverse? "b" -> "b". If we reverse, it's same.
        # Step 2 (len 2): prefix "bb". Reverse? "bb" -> "bb". Same.
        # Step 3 (len 3): prefix "bba". Reverse? "abb". 
        # Step 4 (len 4): prefix "abbb". Reverse? "bbba".
        
        # The example note says: "reverse the second and the third prefix and get a string 'abbb'".
        # Initial: b b a b
        # Reverse prefix 2 (indices 0,1): "b b" -> "b b". String remains "b b a b".
        # Reverse prefix 3 (indices 0,1,2): "b b a" -> "a b b". String becomes "a b b b".
        # Result: "abbb".
        
        # Why did they reverse prefix 2 if it didn't change anything? 
        # Maybe my understanding of "prefix" is wrong? 
        # "prefixes with lengths from 1 to the length of the word"
        # "for each prefix she will either reverse this prefix or leave it as it is"
        # "She will consider the prefixes in the fixed order: from the shortest to the largest."
        
        # Perhaps the decision is not just based on immediate gain, but the state evolves.
        # However, note that reversing a prefix [0..i] when it is symmetric (like "bb") doesn't change the string.
        # So doing it or not doing it is equivalent for the string state.
        # But the problem asks for ANY valid sequence.
        
        # Let's try to understand the greedy logic.
        # At step i (0-indexed, so prefix length i+1), we have a current string.
        # We look at the first character of the current prefix (index 0) and the last character of the current prefix (index i).
        # If char[0] == 'a' and char[i] == 'b', reversing the prefix puts 'b' at the front, which is worse. So we don't reverse.
        # If char[0] == 'b' and char[i] == 'a', reversing the prefix puts 'a' at the front, which is better. So we reverse.
        # If they are the same, reversing doesn't change the first character, so it doesn't affect lexicographical order at index 0.
        # Does it affect deeper characters? Yes, but since we are processing from left to right, and future operations 
        # will reverse longer prefixes, the relative order of characters within the prefix 0..i might be adjusted later.
        # However, the standard solution for this problem is indeed: 
        # Compare s[0] and s[i] of the CURRENT string. If s[0] > s[i] (i.e., 'b' > 'a'), then reverse. Else don't.
        # Why? Because we want the smallest character at index 0. 
        # If current s[0] is 'b' and s[i] is 'a', we can swap them to the front. 
        # If s[0] is 'a', we are already good at index 0. Reversing would put 'a' (from s[i]) at front? No, if s[0]=='a', then s[i] could be 'a' or 'b'.
        # If s[0]=='a' and s[i]=='b', reversing puts 'b' at front -> worse.
        # If s[0]=='a' and s[i]=='a', reversing keeps 'a' at front -> same.
        # So the rule is: if current s[0] == 'b' and current s[i] == 'a', reverse.
        
        # Let's re-trace "bbab" with this rule:
        # Initial: b b a b
        # i=0: s[0]='b', s[0]='b'. Equal. Don't reverse. res[0]=0. String: b b a b.
        # i=1: s[0]='b', s[1]='b'. Equal. Don't reverse? 
        # But example output says reverse prefix 2 (index 1). 
        # Wait, if we don't reverse at i=1, string is still "bbab".
        # i=2: s[0]='b', s[2]='a'. 'b' > 'a'. Reverse prefix 0..2 ("bba" -> "abb"). 
        # String becomes "a b b b". res[2]=1.
        # i=3: s[0]='a', s[3]='b'. 'a' < 'b'. Don't reverse. res[3]=0.
        # Result: 0 0 1 0.
        # This gives "abbb". Same result as example.
        # The example output is 0 1 1 0. Let's see what that does.
        # Initial: b b a b
        # i=0: 0 -> b b a b
        # i=1: 1 -> reverse "bb" -> b b a b (no change)
        # i=2: 1 -> reverse "bba" -> a b b b
        # i=3: 0 -> keep "abbb"
        # Result "abbb".
        # So both 0 0 1 0 and 0 1 1 0 yield "abbb". The problem says "print any of them".
        # My greedy logic produced 0 0 1 0. Is that acceptable? Yes.
        # But why did the example choose 0 1 1 0? Maybe just one possibility.
        # However, let's check the second example: "aaaaa"
        # i=0: s[0]='a', s[0]='a'. Equal. Rule says don't reverse? res[0]=0.
        # But example output is 1 0 0 0 1.
        # Let's trace example output for "aaaaa":
        # i=0: 1 -> reverse "a" -> a. Same.
        # i=1: 0 -> keep "aa". Same.
        # ...
        # All operations on "aaaaa" result in "aaaaa".
        # So any sequence is valid.
        
        # Is there a case where my greedy fails?
        # Consider "ba".
        # i=0: s[0]='b', s[0]='b'. Don't reverse. String "ba".
        # i=1: s[0]='b', s[1]='a'. Reverse. String "ab".
        # Result: 0 1. Final "ab". Correct.
        # What if I reversed at i=0? "ba" -> "ab". Then i=1: "ab", s[0]='a', s[1]='b'. Don't reverse. Final "ab".
        # Result: 1 0. Also correct.
        
        # It seems the condition "if current s[0] > current s[i]" is sufficient to get the lexicographically smallest result.
        # Specifically, if s[0] is 'b' and s[i] is 'a', we MUST reverse to put 'a' at the front.
        # If s[0] is 'a', we don't want to reverse because that would put s[i] (which is >= 'a') at front. 
        # If s[i] is 'a', it doesn't matter (both 'a'), so we can choose either. 
        # The example output for "bbab" chose to reverse even when s[0]==s[i] at step 1.
        # My logic: if s[0] > s[i] then reverse, else don't.
        # This produces a valid answer.
        
        # Implementation details:
        # We maintain the current list of characters.
        # At each step i, compare chars[0] and chars[i].
        # If chars[0] == 'b' and chars[i] == 'a': reverse the prefix.
        # Else: do nothing.
        # Record 1 if reversed, 0 otherwise.
        
        if chars[0] == 'b' and chars[i] == 'a':
            res[i] = 1
            # Reverse the prefix 0..i
            chars[0:i+1] = chars[0:i+1][::-1]
        else:
            res[i] = 0
            
    print(*(res))

if __name__ == "__main__":
    solve()