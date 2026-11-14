import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return
    
    n = int(data[0])
    a = []
    for i in range(n):
        a.append(int(data[i+1]))
    
    # Count frequencies of each number
    from collections import Counter
    counts = Counter(a)
    
    # We need to assign each distinct number to either increasing (inc) or decreasing (dec)
    # Constraints:
    # - In inc: each number appears at most once, and if x is in inc, then x+1 can be in inc (but not required to be consecutive)
    #   Actually, strictly increasing means all elements are unique and sorted.
    # - In dec: each number appears at most once, and if x is in dec, then x-1 can be in dec.
    # - If a number appears k times:
    #   - It can be in inc at most once.
    #   - It can be in dec at most once.
    #   - So if count[x] > 2, it's impossible -> NO.
    #   - If count[x] == 2, one must go to inc and one to dec.
    #   - If count[x] == 1, it can go to either, but we must ensure consistency with neighbors.
    
    # Let's determine the set of numbers that MUST go to inc and MUST go to dec.
    # If count[x] == 2: x must be in both.
    # If count[x] == 1: x can be in inc OR dec.
    
    # However, there is a stricter constraint:
    # If x is in inc, then we cannot have x+1 in dec? No, that's fine.
    # The problem is: if x is in inc, then x+1 can be in inc. If x is in dec, then x-1 can be in dec.
    # But if x is in inc, can x+1 be in dec? Yes.
    # The real conflict arises if we try to put x in inc and x+1 in dec, but we also need to put x+1 in inc? No.
    
    # Let's re-evaluate:
    # We have a set of numbers. Each number x with count[x] == 2 must be in both sequences.
    # Each number x with count[x] == 1 must be in exactly one sequence.
    # 
    # Consider the numbers that appear twice. Let S2 be the set of such numbers.
    # For any x in S2, x is in inc and x is in dec.
    # This implies:
    # - If x is in inc, then any y in inc with y > x must be > x.
    # - If x is in dec, then any z in dec with z < x must be < x.
    # 
    # What if we have x and x+1 both in S2?
    # Then x is in inc and dec. x+1 is in inc and dec.
    # This is valid: inc = {..., x, x+1, ...}, dec = {..., x+1, x, ...}.
    # 
    # What if we have x in S2 and x+1 has count 1?
    # x is in inc and dec. x+1 must be in either inc or dec.
    # If x+1 is in inc: then inc has x, x+1. Valid.
    # If x+1 is in dec: then dec has x, x+1. But dec must be strictly decreasing, so x+1 > x. 
    #   So in dec, we would have ... x+1, x ... which is valid (x+1 > x).
    # 
    # So the only hard constraint is: no number appears more than twice.
    # Is that sufficient?
    # Let's check the example: 1 1 2 1 2 -> counts: 1:3, 2:2. Count of 1 is 3 -> NO. Correct.
    # Example: 4 3 1 5 3 -> counts: 1:1, 3:2, 4:1, 5:1.
    #   3 must be in both.
    #   Others can be assigned.
    #   If we put 1 in inc, 4 in inc, 5 in inc -> inc = [1, 4, 5], dec = [3, 2? no 2]. 
    #   Wait, dec must contain 3. If dec = [3], is that valid? Yes.
    #   But we need to use all numbers.
    #   inc = [1, 4, 5], dec = [3]. 
    #   Check: inc sorted: 1, 4, 5 (ok). dec sorted desc: 3 (ok).
    #   But wait, the example output for 4 3 1 5 3 is:
    #   inc: 3
    #   dec: 5 4 3 1
    #   Here 3 is in both. 1, 4, 5 are in dec.
    #   Why not put 1, 4, 5 in inc? 
    #   If inc = [1, 4, 5] and dec = [3], that is also a valid solution.
    #   The problem says "find ANY two suitable initial sequences".
    # 
    # So the strategy:
    # 1. Check if any count > 2. If so, print NO.
    # 2. Identify numbers that appear twice (must be in both).
    # 3. Identify numbers that appear once (can be in inc or dec).
    # 4. We need to assign the "once" numbers such that:
    #    - The set of numbers assigned to inc (including the doubles) forms a strictly increasing sequence.
    #    - The set of numbers assigned to dec (including the doubles) forms a strictly decreasing sequence.
    # 
    # Since the doubles are in both, they don't restrict the "once" numbers directly in terms of order, 
    # EXCEPT that if we put a number x in inc, it must be distinct from other inc numbers (which it is, by definition of set).
    # The only potential issue is if the assignment creates a conflict? 
    # Actually, since we are just partitioning the set of unique numbers into two sets I and D,
    # such that I is strictly increasing (always true for any set of distinct numbers if sorted)
    # and D is strictly decreasing (always true for any set of distinct numbers if sorted descending).
    # 
    # Wait, is that true?
    # "Strictly increasing sequence is a sequence of integers [x1 < x2 < ... < xk]".
    # If I is a set of distinct integers, we can always sort them to form a strictly increasing sequence.
    # Similarly for D.
    # 
    # So the ONLY constraint is that every number must be assigned to at least one sequence.
    # And if a number appears twice, it must be assigned to BOTH.
    # If a number appears once, it must be assigned to EXACTLY ONE.
    # 
    # Is there any case where this is impossible?
    # Suppose we have numbers {1, 2}. Both appear once.
    # Option 1: inc={1, 2}, dec={}. Valid.
    # Option 2: inc={}, dec={2, 1}. Valid.
    # Option 3: inc={1}, dec={2}. Valid.
    # 
    # So it seems the only condition is max(count) <= 2.
    # Let's re-read the problem carefully.
    # "Two integer sequences existed initially — one of them was strictly increasing, and the other one — strictly decreasing."
    # "They were merged into one sequence a. After that sequence a got shuffled."
    # This implies the multiset of a is the union of the multisets of the two sequences.
    # Since the sequences are strictly increasing/decreasing, they have no duplicates within themselves.
    # Therefore, any number appearing in a can appear at most twice (once in inc, once in dec).
    # If a number appears 3 times, it's impossible.
    # 
    # So the algorithm is simply:
    # 1. Count frequencies. If any > 2, return NO.
    # 2. Construct inc and dec.
    #    - For each number x:
    #      - If count[x] == 2: add x to inc and x to dec.
    #      - If count[x] == 1: we can add x to inc OR dec.
    #        Does it matter?
    #        The problem asks for ANY valid split.
    #        We can greedily assign all "once" numbers to inc?
    #        Then inc = {all numbers with count >= 1}, dec = {all numbers with count == 2}.
    #        Is this valid?
    #        inc will be a set of distinct numbers -> can be sorted to be strictly increasing.
    #        dec will be a set of distinct numbers (only those with count 2) -> can be sorted descending to be strictly decreasing.
    #        And the union of multisets matches a.
    #        Yes, this works.
    # 
    # Wait, let's test with an example where this might fail?
    # Suppose a = [1, 2, 1, 2]. counts: 1:2, 2:2.
    # inc = {1, 2}, dec = {1, 2}.
    # inc sorted: 1, 2. dec sorted desc: 2, 1.
    # Union: 1, 2, 1, 2. Matches.
    # 
    # Suppose a = [1, 2, 3]. counts: 1:1, 2:1, 3:1.
    # inc = {1, 2, 3}, dec = {}.
    # Valid.
    # 
    # Suppose a = [3, 2, 1]. counts: 1:1, 2:1, 3:1.
    # inc = {1, 2, 3}, dec = {}.
    # Valid. (Or inc={}, dec={3, 2, 1}).
    # 
    # Is there any constraint I'm missing?
    # "Note that the empty sequence and the sequence consisting of one element can be considered as increasing or decreasing."
    # This is handled.
    # 
    # So the logic holds: if max frequency <= 2, YES, else NO.
    # And we can construct the solution by putting all numbers with freq 2 in both, and all numbers with freq 1 in inc (and none in dec, or we can distribute them arbitrarily).
    # To be safe and simple: put freq 1 in inc.
    # 
    # Let's double check the example 4 3 1 5 3.
    # counts: 1:1, 3:2, 4:1, 5:1.
    # My logic:
    # inc = {1, 3, 4, 5} -> sorted: 1, 3, 4, 5.
    # dec = {3} -> sorted desc: 3.
    # Output:
    # YES
    # 4
    # 1 3 4 5
    # 1
    # 3
    # Is this valid?
    # inc: 1 < 3 < 4 < 5. Yes.
    # dec: 3. Yes.
    # Union: 1, 3, 4, 5, 3 -> 1, 3, 3, 4, 5. Matches input multiset.
    # The example output was different, but the problem says "any two suitable".
    # 
    # Wait, is there a case where putting freq 1 in inc causes a problem?
    # No, because inc just needs to be strictly increasing, which any set of distinct numbers can be.
    # 
    # So the code is very simple.

    if any(c > 2 for c in counts.values()):
        print("NO")
        return
    
    inc_set = set()
    dec_set = set()
    
    # We need to output the sequences as lists.
    # inc: all numbers with count >= 1 (since we put freq 1 here too)
    # dec: all numbers with count == 2
    
    # Actually, to be absolutely sure, let's consider if we should distribute freq 1 numbers.
    # It doesn't matter. Putting them all in inc is fine.
    
    # Collect numbers
    # We need to handle the output format carefully.
    
    # Let's build the lists
    inc_list = []
    dec_list = []
    
    # We iterate over sorted unique keys to make it deterministic, though not required.
    unique_nums = sorted(counts.keys())
    
    for x in unique_nums:
        c = counts[x]
        if c == 2:
            inc_list.append(x)
            dec_list.append(x)
        elif c == 1:
            inc_list.append(x)
            # dec_list does not get x
    
    # Sort inc_list (it's already sorted by iteration, but let's be explicit)
    inc_list.sort()
    # Sort dec_list descending
    dec_list.sort(reverse=True)
    
    print("YES")
    print(len(inc_list))
    print(*(inc_list))
    print(len(dec_list))
    print(*(dec_list))

if __name__ == '__main__':
    solve()