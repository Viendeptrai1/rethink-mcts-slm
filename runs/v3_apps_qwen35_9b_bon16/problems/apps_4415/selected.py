import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return
    
    n = int(data[0])
    a = []
    for i in range(n):
        a.append(int(data[1 + i]))
    
    if n == 0:
        print("YES")
        print(0)
        print()
        print(0)
        print()
        return

    # Count frequencies of each number
    from collections import Counter
    freq = Counter(a)
    
    # Map: value -> count of occurrences
    counts = {}
    for x in freq:
        counts[x] = freq[x]
    
    # Determine which numbers appear more than once.
    # Each number can appear at most twice (once in increasing, once in decreasing).
    # If any number appears more than twice, it's impossible -> NO
    for x, c in counts.items():
        if c > 2:
            print("NO")
            return
    
    # We need to assign each occurrence to either 'inc' or 'dec'.
    # Strategy:
    # - Sort unique numbers.
    # - Numbers appearing once can go to either, but we need to maintain strict monotonicity.
    # - Numbers appearing twice must go one to inc and one to dec.
    # 
    # Greedy approach:
    # Let's try to put as many numbers as possible into the increasing sequence,
    # and the rest into the decreasing sequence, ensuring constraints.
    #
    # However, a more robust method:
    # Since we can reorder arbitrarily, we just need to partition the multiset.
    # 
    # Observation:
    # If a number x appears twice, one instance MUST be in 'inc' and one in 'dec'.
    # If a number x appears once, we have a choice.
    #
    # Let's construct:
    # inc_sequence: will contain unique numbers in increasing order.
    # dec_sequence: will contain unique numbers in decreasing order.
    # But wait, if a number appears twice, it goes to BOTH.
    # So inc will have {x} and dec will have {x}.
    # 
    # The constraint is:
    # inc: strictly increasing -> all elements in inc must be distinct.
    # dec: strictly decreasing -> all elements in dec must be distinct.
    # Therefore, no number can appear more than once in inc, and no number can appear more than once in dec.
    # This confirms the max frequency is 2.
    #
    # Now, how to assign the single-occurrence numbers?
    # Let S be the set of numbers that appear exactly once.
    # Let D be the set of numbers that appear exactly twice.
    #
    # For x in D: x must be in inc AND x must be in dec.
    # For x in S: x can be in inc OR in dec (or both? No, if we put it in both, frequency becomes 2, but it's only 1 in input. So exactly one).
    #
    # So we need to partition S into S_inc and S_dec such that:
    # - If we add S_inc to D, the resulting set D U S_inc can form a strictly increasing sequence.
    #   This is always true if we sort them, as long as there are no duplicates. Since S has unique numbers and D has unique numbers, D U S_inc has unique numbers.
    #   Wait, is there any adjacency constraint? No, because we can reorder the sequence a arbitrarily. The problem says "shuffled", so we can output them in any order we want as long as the two subsequences are strictly increasing/decreasing.
    #   Actually, the problem says "find any two suitable initial sequences". The initial sequences were strictly increasing/decreasing. Then they were merged and shuffled.
    #   So we just need to output two sequences: one strictly increasing, one strictly decreasing, such that their multiset union equals input 'a'.
    #
    # Constraints recap:
    # 1. inc must be strictly increasing => all elements in inc are unique.
    # 2. dec must be strictly decreasing => all elements in dec are unique.
    # 3. Union of multisets must equal input.
    #
    # This implies:
    # - If count(x) == 2, then x must be in inc and x must be in dec.
    # - If count(x) == 1, then x must be in inc OR in dec (exclusive).
    # - If count(x) > 2, impossible.
    #
    # Is there any other constraint?
    # No. Because if we have a set of unique numbers, we can always arrange them in increasing order.
    # Same for decreasing.
    # The only potential issue is if the problem implied the original sequences had specific values that constrain the split based on neighbors? 
    # Re-reading: "Two integer sequences existed initially... They were merged into one sequence a. After that sequence a got shuffled."
    # "Your task is to find any two suitable initial sequences."
    # This means we just need to reconstruct the two sequences. The shuffling means the relative order in 'a' doesn't matter. We just need to partition the multiset into two sets with no duplicates within each set.
    #
    # So the logic is extremely simple:
    # 1. Check max frequency <= 2.
    # 2. Put all numbers with frequency 2 into both lists.
    # 3. For numbers with frequency 1, we can put them arbitrarily.
    #    However, we need to output them sorted.
    #    Let's just put all frequency-1 numbers into the increasing sequence? 
    #    Then the increasing sequence will be: (all freq-1 numbers) + (all freq-2 numbers).
    #    Wait, if we mix them, we need to sort the whole inc list. Since all elements are unique in the inc list, sorting works.
    #    Similarly for dec: (all freq-1 numbers) + (all freq-2 numbers).
    #    But wait, if we put all freq-1 numbers into inc, then dec only has freq-2 numbers.
    #    Is that valid? Yes.
    #    Is it possible that putting some freq-1 into inc and some into dec is required? 
    #    No, because having them in inc doesn't break the "unique" property, nor does having them in dec.
    #    The only constraint is that a number cannot be duplicated in inc, or duplicated in dec.
    #    Since freq-1 numbers appear only once in input, they can go to inc (become unique there) or dec (become unique there).
    #    They just can't go to both.
    #    So we can put ALL freq-1 numbers into inc. Then dec will only have freq-2 numbers.
    #    This is a valid solution.
    #
    # Let's double check with an example where this might fail?
    # Input: 1 2 1 2
    # freq: 1->2, 2->2.
    # inc = [1, 2], dec = [2, 1]. Valid.
    # Input: 1 1 1 -> freq 1->3. NO. Correct.
    # Input: 1 2 3 -> freq 1->1, 2->1, 3->1.
    # inc = [1, 2, 3], dec = []. Valid.
    # Input: 3 2 1 -> freq 1->1, 2->1, 3->1.
    # inc = [1, 2, 3], dec = []. Valid. (Original could have been [3,2,1] and [], or [1,2,3] and []).
    #
    # Wait, is there a case where we MUST split freq-1 numbers?
    # Suppose input is 1 2 3 1 2 3. Freqs: 1->2, 2->2, 3->2.
    # inc = [1, 2, 3], dec = [3, 2, 1]. Valid.
    #
    # What if input is 1 2 100 200 ...
    # It seems putting all single-occurrence numbers into the increasing sequence is always safe.
    # Why? Because the increasing sequence just needs to be strictly increasing. If we take the set of all numbers that appear once, plus all numbers that appear twice, the set of values in 'inc' will have no duplicates (since we take at most one copy of each number). We can sort this set to form a strictly increasing sequence.
    # Similarly, 'dec' will contain the numbers that appear twice. This set also has no duplicates. We can sort it in reverse to form a strictly decreasing sequence.
    #
    # Is there any constraint I missed?
    # "Note that the empty sequence and the sequence consisting of one element can be considered as increasing or decreasing."
    # Yes, handled.
    #
    # Wait, what if the problem implies that the two original sequences were non-empty? 
    # "Note that the empty sequence ... can be considered". So empty is allowed.
    #
    # Let's re-read carefully: "One of them should be strictly increasing and the other one — strictly decreasing."
    # It doesn't say both must be non-empty.
    #
    # So the algorithm:
    # 1. Count frequencies.
    # 2. If any freq > 2, print NO.
    # 3. Identify numbers with freq 2 (must be in both).
    # 4. Identify numbers with freq 1 (can be in inc).
    # 5. inc_set = set(freq2_numbers) U set(freq1_numbers)
    # 6. dec_set = set(freq2_numbers)
    # 7. Sort inc_set ascending, dec_set descending.
    # 8. Print YES and the sequences.
    #
    # Let's test this logic on the provided examples.
    # Ex 1: 7 2 7 3 3 1 4
    # Freqs: 7:2, 2:1, 3:2, 1:1, 4:1.
    # freq2: {7, 3}. freq1: {2, 1, 4}.
    # inc_set = {7, 3, 2, 1, 4} -> sorted: 1, 2, 3, 4, 7.
    # dec_set = {7, 3} -> sorted desc: 7, 3.
    # Output:
    # YES
    # 5
    # 1 2 3 4 7
    # 2
    # 7 3
    # The example output is different but says "any two suitable". My solution is valid.
    # Wait, the example output has inc: 3 7 (len 2) and dec: 7 4 3 2 1 (len 5).
    # Union: {3,7} U {7,4,3,2,1} = {1,2,3,3,4,7,7}. Matches input.
    # My solution: inc: 1,2,3,4,7; dec: 7,3. Union: {1,2,3,3,4,7,7}. Matches.
    # Both valid.
    #
    # Ex 3: 1 1 2 1 2
    # Freqs: 1:3, 2:2.
    # 1 appears 3 times -> NO. Correct.
    #
    # Ex 4: 0 1 2 3 4
    # Freqs: all 1.
    # freq2: {}. freq1: {0,1,2,3,4}.
    # inc: 0 1 2 3 4. dec: [].
    # Example output: inc empty, dec 4 3 2 1 0. Also valid.
    #
    # Is there any case where putting all freq-1 into inc fails?
    # No, because the only constraint on inc is uniqueness and ordering. Uniqueness is guaranteed by taking at most one instance of each number. Ordering is guaranteed by sorting.
    # Same for dec.
    #
    # Wait, is it possible that the judge expects a specific split? "find ANY two". So my split is fine.
    #
    # Implementation details:
    # Read n.
    # Read array.
    # Counter.
    # Check max freq.
    # Build lists.
    # Print.

    # Corner case: n=1.
    # a = [5]. freq 5:1.
    # inc = [5], dec = []. YES.
    # Or inc=[], dec=[5]. YES.
    # My logic: inc=[5], dec=[]. Valid.

    # One more check: Is it possible that the problem considers "strictly increasing" to require length >= 2?
    # "Note that the empty sequence and the sequence consisting of one element can be considered as increasing or decreasing."
    # So length 0 or 1 is fine.

    # Code structure:
    # Read all tokens.
    # Parse n.
    # Parse a.
    # Logic.
    # Print.

    # Optimization: n up to 2*10^5. Sorting is O(N log N), Counter is O(N). Fine.

    counts = {}
    for x in a:
        if x in counts:
            counts[x] += 1
        else:
            counts[x] = 1

    for x, c in counts.items():
        if c > 2:
            print("NO")
            return

    # Separate numbers
    freq2 = []
    freq1 = []
    
    for x, c in counts.items():
        if c == 2:
            freq2.append(x)
        else:
            freq1.append(x)
            
    # Sort for output
    freq2.sort()
    freq1.sort()
    
    # Construct increasing sequence
    # All freq2 and all freq1
    inc_list = freq1 + freq2
    # Since freq1 and freq2 are sorted, merging them requires full sort or careful merge.
    # Given N is small enough, just sort the combined list.
    inc_list.sort()
    
    # Construct decreasing sequence
    # Only freq2
    dec_list = freq2
    dec_list.sort(reverse=True)
    
    print("YES")
    print(len(inc_list))
    print(*(inc_list))
    print(len(dec_list))
    print(*(dec_list))

solve()