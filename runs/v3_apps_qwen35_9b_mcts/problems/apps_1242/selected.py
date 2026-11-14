import sys

def solve():
    s = sys.stdin.readline().strip()
    n = len(s)
    res = []
    
    # We simulate the process from i = 1 to n.
    # At each step i, we consider the current state of the string.
    # We have two choices: reverse prefix i or not.
    # We want to choose the option that leads to the lexicographically smallest result eventually.
    # However, a key observation is that the decision at step i only affects the relative order of the first i characters.
    # Specifically, if we look at the current string state before step i, let's call it T.
    # If we reverse prefix i, the new string becomes T[0...i-1] reversed + T[i...].
    # The crucial insight for this specific problem (Codeforces 1141C / similar logic) is:
    # We can greedily decide. But actually, there is a simpler invariant.
    # Let's trace the effect.
    # Actually, the standard solution for this problem relies on the fact that we can determine the final state
    # by looking at the current character and the next one, but since we process prefixes 1..n,
    # we can maintain the current string and try both options? No, n is up to 1000, O(n^2) is fine.
    # But we need to be careful: the choice at step i affects the string for step i+1.
    # However, note the property: reversing prefix i twice is identity.
    # Let's re-evaluate the greedy strategy.
    # Consider the current string S. We are at step i (1-indexed).
    # We can either keep S or reverse S[0:i].
    # Which one is better?
    # Actually, the problem is equivalent to: we can reverse any prefix. We want the lexicographically smallest result.
    # It turns out we can determine the answer by looking at the current character and the next available character in the "sorted" sense?
    # No, let's use the simulation with a greedy choice based on the immediate next character.
    # Wait, the standard solution for "IA and Magnets" (Codeforces 1141C is different, this is likely 1141B? No, this is 1141C is not it. This is Codeforces 1141D? No.
    # This is Codeforces Problem 1141C? No. It is Codeforces 1141B? No.
    # Actually, this is Codeforces 1141C is "Polycarp Restores Permutation".
    # The problem is Codeforces 1141D? No.
    # Let's just solve it logically.
    # We process i from 1 to n.
    # At step i, we have a current string. We can reverse the prefix of length i.
    # We want to minimize the final string.
    # Observation: The relative order of characters in the prefix can be changed arbitrarily by a sequence of reversals?
    # No, we must process in order 1, 2, ..., n.
    # Let's try a different perspective.
    # Suppose we have processed up to i-1. Now we consider prefix i.
    # Let the current string be S.
    # Option 1: Do nothing. S remains S.
    # Option 2: Reverse S[0:i].
    # We need to pick the one that allows us to reach a lexicographically smaller string at the end.
    # However, note that the operations are sequential.
    # There is a known greedy strategy for this specific problem:
    # At step i, look at the current character S[i-1] (0-indexed) and the character that would be at S[i-1] if we reversed the prefix.
    # Actually, let's look at the example: "bbab"
    # i=1: "b". Reverse -> "b". No change. Let's say we don't reverse (0). String: "b".
    # i=2: "bb". Reverse -> "bb". No change.
    # i=3: "bba". Reverse -> "abb". Now string is "abb".
    # i=4: "abba". Reverse -> "abba". No change.
    # Result: 0 0 1 0? But example output is 0 1 1 0.
    # Let's re-read the example note: "reverse the second and the third prefix".
    # Start: "bbab"
    # i=1: prefix "b". Reverse? No. String: "bbab".
    # i=2: prefix "bb". Reverse -> "bb". String: "bbab". (Wait, reversing "bb" gives "bb").
    # i=3: prefix "bba". Reverse -> "abb". String: "abb" + "b" = "abbb".
    # i=4: prefix "abbb". Reverse -> "bbba". String: "bbba".
    # This doesn't match "abbb".
    # Ah, the example says: "reverse the second and the third prefix".
    # Let's trace carefully.
    # Initial: s = "bbab"
    # Step 1 (i=1): Prefix "b". If we reverse, it's "b". If not, "b".
    # Step 2 (i=2): Current string is "bb". Prefix "bb". Reverse -> "bb".
    # Step 3 (i=3): Current string is "bb" + "a" = "bba". Prefix "bba". Reverse -> "abb". String becomes "abb" + "b" = "abbb".
    # Step 4 (i=4): Current string is "abbb". Prefix "abbb". Reverse -> "bbba".
    # Final: "bbba".
    # But the example says the result is "abbb".
    # How?
    # Maybe the operations are cumulative in a way I'm not seeing?
    # "IA will look at all prefixes with lengths from 1 to the length of the word and for each prefix she will either reverse this prefix or leave it as it is. She will consider the prefixes in the fixed order: from the shortest to the largest."
    # This implies sequential updates.
    # Let's re-read the example note carefully.
    # "In the first example, IA can reverse the second and the third prefix and get a string "abbb"."
    # Initial: b b a b
    # i=1: prefix 1 ("b"). Reverse? No (0). String: b b a b.
    # i=2: prefix 2 ("bb"). Reverse? Yes (1). String: b b a b (since "bb" reversed is "bb").
    # i=3: prefix 3 ("bba"). Reverse? Yes (1). String: a b b b.
    # i=4: prefix 4 ("abbb"). Reverse? No (0). String: a b b b.
    # Final: "abbb".
    # Okay, my manual trace was wrong because I thought reversing "bb" changes anything, but it doesn't.
    # So the sequence 0, 1, 1, 0 works.
    # Now, how to decide greedily?
    # At step i, we have a current string S. We can reverse S[0:i] or not.
    # We want to minimize the final string.
    # Is it true that we should reverse if and only if the current last character of the prefix (S[i-1]) is greater than the character that would be there after reversal?
    # Let's check.
    # i=1: S="b". Last char 'b'. Reverse -> 'b'. Equal. Don't reverse? Or doesn't matter.
    # i=2: S="bb". Last char 'b'. Reverse -> 'b'. Equal.
    # i=3: S="bba". Last char 'a'. Reverse -> 'b'. 'a' < 'b'. So if we reverse, the new last char becomes 'b' (which is worse for lexicographical order at the end of the prefix?).
    # Wait, we want the whole string to be small.
    # The decision at step i affects the order of the first i characters.
    # Actually, there is a simpler invariant.
    # Consider the string as a sequence of characters.
    # When we are at step i, we have a current arrangement of the first i characters.
    # We can reverse the whole block of i characters.
    # Notice that the relative order of the first i-1 characters might change, but the set of characters in the first i positions remains the same.
    # However, the key is the position of the smallest character.
    # Let's try a different approach: simulate the process and at each step, check which option (reverse or not) leads to a lexicographically smaller string *at that step*?
    # No, because a locally smaller prefix might lead to a larger suffix later?
    # But wait, the operations are prefix reversals.
    # Actually, the problem is equivalent to: we can reverse any prefix. We want the lexicographically smallest result.
    # It turns out that the optimal strategy is: at step i, reverse the prefix if and only if the current character at index i-1 is 'b' and the character that would be at index i-1 after reversal is 'a'?
    # Let's test this hypothesis on "bbab".
    # i=1: S="b". S[0]='b'. Reverse -> 'b'. No change.
    # i=2: S="bb". S[1]='b'. Reverse -> 'b'. No change.
    # i=3: S="bba". S[2]='a'. Reverse -> 'b'. 'a' < 'b'. If we reverse, the new S[2] becomes 'b'. This seems bad locally.
    # But the example says we SHOULD reverse at i=3.
    # Why? Because reversing "bba" gives "abb". The string becomes "abbb".
    # If we didn't reverse, it would be "bba" + "b" = "bbab".
    # Comparing "abbb" and "bbab": "abbb" is smaller.
    # So even though the last character of the prefix became 'b' (worse), the earlier characters became 'a', 'b' instead of 'b', 'b'.
    # The first difference is at index 0: 'a' vs 'b'.
    # So we should reverse if the reversed prefix is lexicographically smaller than the current prefix?
    # Let's check:
    # i=3: Current prefix "bba". Reversed "abb". "abb" < "bba". So reverse.
    # i=2: Current prefix "bb". Reversed "bb". Equal.
    # i=1: Current prefix "b". Reversed "b". Equal.
    # i=4: Current string "abbb". Prefix "abbb". Reversed "bbba". "abbb" < "bbba". Don't reverse.
    # This matches the example output: 0, 0, 1, 0?
    # Wait, the example output is 0 1 1 0.
    # My trace for i=2: "bb" reversed is "bb". Equal. So 0 or 1?
    # If I output 0 for i=2, and 1 for i=3, I get 0 0 1 0.
    # The example output is 0 1 1 0.
    # Does 0 1 1 0 work?
    # i=1: 0 -> "b"
    # i=2: 1 -> "bb" (no change)
    # i=3: 1 -> "bba" -> "abb" -> "abbb"
    # i=4: 0 -> "abbb"
    # Result "abbb".
    # Does 0 0 1 0 work?
    # i=1: 0 -> "b"
    # i=2: 0 -> "bb"
    # i=3: 1 -> "bba" -> "abb" -> "abbb"
    # i=4: 0 -> "abbb"
    # Result "abbb".
    # Both work. The problem says "print any of them".
    # So the strategy "reverse if reversed_prefix < current_prefix" seems valid.
    # Let's verify with the second example: "aaaaa".
    # i=1: "a" vs "a". Equal.
    # i=2: "aa" vs "aa". Equal.
    # ...
    # All equal. We can output all 0s or all 1s or mixed.
    # Example output: 1 0 0 0 1.
    # My strategy would output 0 0 0 0 0 (if strict less) or maybe 1 if I use <=?
    # The problem says "lexicographically smallest". If equal, it doesn't matter.
    # So the algorithm is:
    # current_s = s
    # for i from 1 to n:
    #   prefix = current_s[:i]
    #   reversed_prefix = prefix[::-1]
    #   if reversed_prefix < prefix:
    #     current_s = reversed_prefix + current_s[i:]
    #     res.append(1)
    #   else:
    #     res.append(0)
    #
    # Let's double check if this greedy works.
    # Is it possible that reversing a prefix that is NOT smaller now leads to a better result later?
    # Suppose we have "ba".
    # i=1: "b" vs "b". Equal.
    # i=2: "ba" vs "ab". "ab" < "ba". Reverse. Result "ab".
    # Correct.
    # Suppose we have "ab".
    # i=1: "a" vs "a".
    # i=2: "ab" vs "ba". "ab" < "ba". Don't reverse. Result "ab".
    # Correct.
    # What if we have "bba"?
    # i=1: "b" -> "b".
    # i=2: "bb" -> "bb".
    # i=3: "bba" -> "abb". Reverse.
    # Result "abb".
    # Is there a case where we should reverse even if reversed_prefix >= current_prefix?
    # Suppose current_prefix = "ab", reversed = "ba". "ab" < "ba". We don't reverse.
    # If we reversed, we get "ba". Then next step i+1, we have "ba" + ...
    # If we didn't reverse, we have "ab" + ...
    # Since "ab..." is lexicographically smaller than "ba..." regardless of the suffix (because the first difference is at index 0 or 1), keeping "ab" is always better than "ba" for the final string comparison, assuming the suffix is the same.
    # But wait, the suffix is NOT the same. The suffix starts at index i.
    # However, the operation at step i only permutes the first i characters. The characters from i to n-1 are untouched.
    # So the suffix s[i:] is constant regardless of the decision at step i.
    # Therefore, to minimize the final string, we must minimize the prefix of length i at step i.
    # Because the final string is (prefix of length i) + (suffix).
    # Comparing two strings A + S and B + S, if A < B, then A+S < B+S.
    # So the greedy choice is locally optimal and globally optimal.
    # We simply need to minimize the prefix of length i at each step i.
    # So the algorithm is correct.

    current_s = list(s)
    res = []
    for i in range(1, n + 1):
        # Extract current prefix
        # We can work with the list directly
        # prefix is current_s[0:i]
        # reversed_prefix is current_s[0:i][::-1]
        # Compare them lexicographically
        
        # Optimization: we don't need to construct the full reversed string if we can compare on the fly,
        # but n=1000, so O(n^2) is perfectly fine.
        
        prefix = current_s[:i]
        rev_prefix = prefix[::-1]
        
        if rev_prefix < prefix:
            # Reverse
            current_s[:i] = rev_prefix
            res.append(1)
        else:
            res.append(0)
            
    print(*(res))

if __name__ == '__main__':
    solve()