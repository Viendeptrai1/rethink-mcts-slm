import sys

def solve():
    s = sys.stdin.readline().strip()
    t = sys.stdin.readline().strip()

    # To make s' as small as possible lexicographically, sort s in ascending order.
    # To make t' as large as possible lexicographically, sort t in ascending order.
    # If the smallest possible s' is strictly less than the largest possible t', then it's possible.
    # However, the condition for lexicographic order s' < t' can be satisfied if we can arrange
    # characters such that at the first differing position, s'[i] < t'[i], or if s' is a proper prefix of t'.
    
    # Actually, the optimal strategy is:
    # 1. Sort s to get the smallest possible string s_min.
    # 2. Sort t to get the smallest possible string t_min? 
    #    Wait, we want to maximize the chance that s' < t'.
    #    The best way to ensure s' < t' is:
    #    - Make s' as small as possible (sort s ascending).
    #    - Make t' as large as possible? Not necessarily. 
    #      Consider: s = "b", t = "a". Sorted s="b", sorted t="a". "b" < "a" is False.
    #      But we can't rearrange to make "b" < "a" because there's only one char.
    #
    #    Let's reconsider:
    #    We want to know if there exist permutations s' and t' such that s' < t'.
    #    This is possible if and only if the smallest possible s' is less than the largest possible t'?
    #    No. Example: s="y", t="x". s_min="y", t_max="x". "y" < "x" is False. Correct.
    #    Example: s="a", t="b". s_min="a", t_max="b". "a" < "b" is True. Correct.
    #    Example: s="yx", t="axy". 
    #      s_min = "xy"
    #      t_min = "axy", t_max = "yxa" (descending).
    #      Is "xy" < "yxa"? Yes.
    #
    #    Actually, the condition simplifies to:
    #    If we sort s in ascending order to get s_sorted, and sort t in ascending order to get t_sorted,
    #    does s_sorted < t_sorted hold?
    #    Not exactly. We want to check if there EXISTS a pair.
    #    The easiest way to satisfy s' < t' is to make s' as small as possible and t' as "large" as possible in a way that helps.
    #    However, note the definition:
    #    Case 1: s' is a prefix of t' and len(s') < len(t').
    #    Case 2: At first diff index i, s'[i] < t'[i].
    #
    #    Strategy:
    #    To maximize the chance of s' < t':
    #    - Construct s' by sorting s in ascending order (smallest possible).
    #    - Construct t' by sorting t in ascending order? 
    #      If we sort both in ascending order, we get the "lexicographically smallest" versions.
    #      If s_sorted < t_sorted, then we have found a valid pair (s_sorted, t_sorted).
    #      Is it possible that s_sorted >= t_sorted but there exists another pair?
    #      Suppose s_sorted >= t_sorted. Since s_sorted is the smallest permutation of s, any other s'' >= s_sorted.
    #      Since t_sorted is the smallest permutation of t, any other t''' >= t_sorted.
    #      This doesn't immediately imply impossibility.
    #
    #    Let's try a different approach.
    #    We want s' < t'.
    #    Consider the smallest possible s' (s_sorted_asc) and the largest possible t' (t_sorted_desc).
    #    If s_sorted_asc < t_sorted_desc, then Yes.
    #    Is this condition necessary?
    #    Suppose s_sorted_asc >= t_sorted_desc.
    #    Then for any s' (permutation of s), s' >= s_sorted_asc >= t_sorted_desc >= t' (permutation of t).
    #    So s' >= t' for all pairs. Thus, if s_sorted_asc >= t_sorted_desc, the answer is No.
    #    Conversely, if s_sorted_asc < t_sorted_desc, then we have a valid pair (s_sorted_asc, t_sorted_desc), so Yes.
    #
    #    Therefore, the condition is: sort s ascending, sort t descending, check if s < t.
    
    s_sorted = sorted(s)
    t_sorted = sorted(t, reverse=True)
    
    s_str = "".join(s_sorted)
    t_str = "".join(t_sorted)
    
    if s_str < t_str:
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    solve()