import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        n = int(next(iterator))
        k = int(next(iterator))
        a = []
        for _ in range(n):
            a.append(int(next(iterator)))
    except StopIteration:
        return

    if k == 1:
        # If k=1, no two distinct numbers can satisfy y = x*1 (since x != y), 
        # but the problem says "no pair ... such that y = x*k". 
        # If k=1, then y=x, but the set has distinct integers, so no pair exists.
        # However, the standard interpretation for k=1 in this specific problem type 
        # (often seen in competitive programming) is that you cannot have both x and x*k.
        # Since x*k = x, this would imply we can't have x and x, which is impossible in a set.
        # BUT, re-reading the definition: "no pair of integers where one is equal to another integer multiplied by k".
        # If k=1, then for any x, x = x*1. Does this count as a pair? The pair must be two integers from the set.
        # Usually, in these problems, if k=1, the answer is 0 because every element x forms a conflict with itself?
        # No, the problem says "pair of integers x and y (x < y)". If x < y, then x cannot equal y.
        # So if k=1, y = x*1 => y=x, which contradicts x < y. Thus, for k=1, there are NO conflicts.
        # The entire set is valid.
        print(n)
        return

    # Sort the array to process from smallest to largest
    a.sort()
    
    # Use a set for O(1) lookups
    present = set(a)
    
    # We will count how many we can keep.
    # Strategy: Iterate through the sorted array. If we encounter a number x,
    # and we have already decided to keep x/k (if it exists in the set), then we cannot keep x.
    # Otherwise, we keep x.
    # To implement this efficiently:
    # We can maintain a set of "kept" numbers.
    # When we see x, check if x/k is in the kept set.
    # If yes, skip x. If no, add x to kept set.
    
    kept = set()
    count = 0
    
    for x in a:
        # Check if x is a multiple of k and if x/k is in our kept set
        if x % k == 0:
            prev = x // k
            if prev in kept:
                # Conflict: prev is kept, so we cannot keep x
                continue
        # If no conflict, keep x
        kept.add(x)
        count += 1
        
    print(count)

if __name__ == '__main__':
    solve()