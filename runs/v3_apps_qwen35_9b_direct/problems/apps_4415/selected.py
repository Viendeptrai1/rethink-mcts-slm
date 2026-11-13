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
    
    # Count frequencies of each number
    from collections import Counter
    counts = Counter(a)
    
    # Find the maximum frequency
    max_freq = 0
    for x in counts:
        if counts[x] > max_freq:
            max_freq = counts[x]
    
    # If any number appears more than twice, it's impossible
    if max_freq > 2:
        print("NO")
        return
    
    # We need to assign each occurrence of a number to either increasing or decreasing.
    # Strategy:
    # 1. Numbers appearing once: can go to either. Let's put them in increasing first to save decreasing slots? 
    #    Actually, a better greedy approach:
    #    - Numbers appearing twice MUST be split: one in increasing, one in decreasing.
    #    - Numbers appearing once can go to either.
    #
    # To maximize chances, we should try to balance or follow a specific pattern.
    # Let's try:
    # - For numbers with count 2: one goes to inc, one to dec.
    # - For numbers with count 1: we can assign them to inc if inc is not "full" in terms of value constraints?
    #   Actually, since we can reorder the output sequences, the only constraint is:
    #   inc must be strictly increasing, dec must be strictly decreasing.
    #   This means in the final inc list, all elements must be unique and sorted.
    #   In the final dec list, all elements must be unique and sorted descending.
    #
    # So the problem reduces to:
    # Can we partition the multiset of numbers into two sets S_inc and S_dec such that:
    # - All elements in S_inc are distinct.
    # - All elements in S_dec are distinct.
    # - S_inc U S_dec = original multiset.
    #
    # This is possible if and only if no number appears more than twice.
    # If a number appears twice, one copy goes to S_inc, one to S_dec.
    # If a number appears once, it can go to either.
    #
    # So the condition is simply max_freq <= 2.
    # If max_freq <= 2, we can always construct a solution.
    #
    # Construction:
    # 1. Identify numbers with count 2. They must be split.
    # 2. Identify numbers with count 1. We can assign them arbitrarily, but we need to ensure the resulting lists are valid.
    #    Since we can sort the lists, any set of distinct numbers can form a valid strictly increasing sequence.
    #    Similarly for decreasing.
    #
    # So the algorithm is:
    # - Create a list for inc and a list for dec.
    # - Iterate through unique numbers.
    # - If count is 2: add one to inc, one to dec.
    # - If count is 1: add to inc (or dec, doesn't matter for validity as long as distinct).
    #   Let's add to inc to keep inc as large as possible? Or balance?
    #   Actually, it doesn't matter. Just add to inc.
    #
    # Wait, is there any constraint I missed?
    # "Strictly increasing" and "Strictly decreasing".
    # Yes, just distinct elements in each.
    #
    # Let's verify with an example:
    # Input: 1 1 2 1 2 -> counts: {1:3, 2:2}. Max freq 3 -> NO. Correct.
    # Input: 7 2 7 3 3 1 4 -> counts: {7:2, 2:1, 3:2, 1:1, 4:1}.
    #   7: split -> inc: [7], dec: [7]
    #   2: count 1 -> inc: [7, 2] (will sort later)
    #   3: split -> inc: [7, 2, 3], dec: [7, 3]
    #   1: count 1 -> inc: [7, 2, 3, 1]
    #   4: count 1 -> inc: [7, 2, 3, 1, 4]
    #   Sort inc: [1, 2, 3, 4, 7] -> strictly increasing.
    #   Sort dec desc: [7, 3] -> strictly decreasing.
    #   Union: {1,2,3,4,7,7,3} -> matches input multiset.
    #
    # So the logic holds.
    
    if max_freq > 2:
        print("NO")
        return
    
    inc = []
    dec = []
    
    # We need to handle the counts.
    # Let's iterate over the unique numbers.
    # To make it deterministic and simple:
    # For each number x:
    #   if count[x] == 2:
    #       inc.append(x)
    #       dec.append(x)
    #   elif count[x] == 1:
    #       inc.append(x)
    #       # dec gets nothing from this number
    
    # But wait, what if we assign count=1 numbers to dec instead?
    # It doesn't matter for correctness because both resulting sets will have distinct elements.
    # However, we must ensure we use all elements.
    # The above logic uses all elements:
    #   count=2: 1 in inc, 1 in dec. Total 2.
    #   count=1: 1 in inc. Total 1.
    # Sum of counts = sum(counts) = n.
    # So all elements are used.
    
    # Let's implement this.
    
    # We can iterate over the sorted unique keys to have deterministic output, though not required.
    unique_nums = sorted(counts.keys())
    
    for x in unique_nums:
        c = counts[x]
        if c == 2:
            inc.append(x)
            dec.append(x)
        elif c == 1:
            inc.append(x)
        # c cannot be 0 or >2 based on checks
    
    # Now sort inc in ascending order
    inc.sort()
    # Sort dec in descending order
    dec.sort(reverse=True)
    
    print("YES")
    print(len(inc))
    print(*(inc))
    print(len(dec))
    print(*(dec))

if __name__ == '__main__':
    solve()