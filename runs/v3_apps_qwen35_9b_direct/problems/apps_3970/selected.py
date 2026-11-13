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
        # If k is 1, then for any x, x*1 = x. Since all numbers are distinct,
        # we cannot have both x and x in the set. But the problem says "no pair of integers x and y (x < y) such that y = x*k".
        # If k=1, then y = x*1 => y = x. But the condition requires x < y, so y cannot equal x.
        # Therefore, if k=1, there are no pairs (x, y) with x < y such that y = x*1 because that would imply x=y.
        # So the entire set is k-multiple free.
        print(n)
        return

    # Sort the array to process in increasing order
    a.sort()

    # Use a set for O(1) lookups
    present = set(a)
    
    # We will count how many numbers we keep.
    # Strategy: For each number, if it is part of a chain x, x*k, x*k^2..., we must pick at most one from each "conflict group" in a specific way.
    # Actually, a simpler greedy approach works:
    # Iterate through the sorted numbers. If a number x is present, and x/k is also present and x/k is a multiple of k (i.e., x % k == 0), then x conflicts with x/k.
    # However, the conflict is symmetric in terms of existence but directional in value.
    # Let's rephrase: We have chains like {v, v*k, v*k^2, ...}. In each chain, we cannot pick adjacent elements.
    # To maximize the subset size, in a chain of length L, we can pick ceil(L/2) elements? No, that's for independent set on a path.
    # Wait, the condition is: no x, y such that y = x*k.
    # This means in a chain v, v*k, v*k^2, v*k^3, ... we cannot have both v and v*k, nor v*k and v*k^2, etc.
    # This is exactly the Maximum Independent Set on a path graph where edges are (v, v*k), (v*k, v*k^2), etc.
    # For a path of L nodes, the max independent set size is ceil(L/2).
    # BUT, we can solve this greedily by processing from smallest to largest.
    # If we encounter a number x, and x/k is in our set, we have a conflict.
    # Actually, a better greedy strategy:
    # Iterate from smallest to largest. If x is present and x/k is present, then we have a conflict between x and x/k.
    # Since we process in increasing order, when we are at x, x/k (if it exists) has already been processed.
    # If we kept x/k, we cannot keep x. If we didn't keep x/k, we can keep x.
    # To maximize the total count, if we have a choice, which one should we keep?
    # Consider the chain: v, v*k, v*k^2.
    # If we keep v, we can't keep v*k. Then we can keep v*k^2. Total 2.
    # If we don't keep v, we can keep v*k. Then we can't keep v*k^2. Total 1.
    # So it seems beneficial to keep the smaller one?
    # Let's check: v, v*k, v*k^2, v*k^3.
    # Keep v -> skip v*k -> keep v*k^2 -> skip v*k^3. Count = 2.
    # Skip v -> keep v*k -> skip v*k^2 -> keep v*k^3. Count = 2.
    # It seems the count is the same for even length.
    # For odd length (3): Keep v, skip vk, keep vk^2 -> 2. Skip v, keep vk, skip vk^2 -> 1.
    # So keeping the smaller element is better for odd length chains.
    # What about disjoint chains? The decision in one chain doesn't affect others.
    # So the strategy: Iterate from smallest to largest. If x is present and x % k == 0 and (x // k) is present, then we have a conflict with x//k.
    # Since we process in order, x//k was processed earlier.
    # If we decided to keep x//k, we must discard x.
    # If we decided to discard x//k, we can keep x.
    # But wait, the decision to keep x//k might have been forced by x//k^2? No, x//k^2 is smaller than x//k.
    # Let's trace the logic carefully.
    # We want to select a subset S such that no two elements have ratio k.
    # This is equivalent to finding the maximum independent set on a collection of disjoint paths.
    # The paths are formed by dividing each number by k repeatedly until it's not divisible by k.
    # For each starting number v (where v % k != 0), the chain is v, v*k, v*k^2, ...
    # We can solve each chain independently.
    # For a chain of length L, the max independent set size is ceil(L/2).
    # However, we don't need to explicitly build chains. We can use a greedy approach with a set of "kept" numbers.
    # Algorithm:
    # 1. Sort the array.
    # 2. Maintain a set `kept` of numbers we have decided to include.
    # 3. Iterate x in sorted array:
    #    If x is in `kept`, we have a conflict? No, `kept` contains numbers we decided to keep.
    #    The conflict is between x and x/k.
    #    If x % k == 0 and (x // k) is in `kept`, then we cannot keep x.
    #    Otherwise, we can keep x.
    #    Wait, is this correct?
    #    Example: 2, 4, 8 with k=2.
    #    Sorted: 2, 4, 8.
    #    x=2: 2%2==0? Yes. 2//2=1. Is 1 in kept? No. Keep 2. kept={2}.
    #    x=4: 4%2==0? Yes. 4//2=2. Is 2 in kept? Yes. Conflict! Do not keep 4.
    #    x=8: 8%2==0? Yes. 8//2=4. Is 4 in kept? No. Keep 8. kept={2, 8}.
    #    Result size 2. Correct ({2, 8}).
    #    Example: 2, 4, 8, 16 with k=2.
    #    x=2: Keep. kept={2}.
    #    x=4: 2 in kept? Yes. Skip.
    #    x=8: 4 in kept? No. Keep. kept={2, 8}.
    #    x=16: 8 in kept? Yes. Skip.
    #    Result size 2. Correct ({2, 8} or {4, 16}).
    #    Example: 3, 6, 12 with k=2.
    #    x=3: 3%2!=0. Keep. kept={3}.
    #    x=6: 6%2==0, 3 in kept? Yes. Skip.
    #    x=12: 12%2==0, 6 in kept? No. Keep. kept={3, 12}.
    #    Result size 2. Correct.
    #    This greedy strategy works because for any chain v, v*k, v*k^2..., the decision at v*k depends on v. If v is kept, v*k is skipped. If v is skipped, v*k is kept (unless v*k conflicts with v*k^2? No, v*k^2 depends on v*k).
    #    Wait, if v is skipped, we keep v*k. Then v*k^2 will see v*k in kept and skip it.
    #    So the pattern is Keep, Skip, Keep, Skip... starting from the smallest.
    #    This yields ceil(L/2) which is optimal.
    
    kept = set()
    count = 0
    
    for x in a:
        if x % k == 0:
            prev = x // k
            if prev in kept:
                # Conflict with a previously kept number
                continue
        # If no conflict, add to kept
        kept.add(x)
        count += 1
        
    print(count)

if __name__ == '__main__':
    solve()