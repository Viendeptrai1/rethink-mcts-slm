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
        # If k is 1, no two distinct numbers can satisfy y = x * 1 because they must be distinct.
        # However, the definition says "no pair ... such that y = x * k".
        # If k=1, then y=x, but the set has distinct integers, so no such pair exists.
        # Wait, let's re-read carefully: "no two integers x and y (x < y) ... such that y = x * k".
        # If k=1, then y = x. But x < y implies x < x, which is impossible.
        # So if k=1, the entire set is k-multiple free.
        print(n)
        return

    s = set(a)
    
    # We need to select a subset such that we don't have both x and x*k.
    # This is a maximum independent set problem on a collection of disjoint chains.
    # For a given number x, if x*k exists in the set, they form a conflict.
    # We can decompose the numbers into chains: x, x*k, x*k^2, ...
    # For each chain, we want to pick the maximum number of elements such that no two are adjacent (in the chain sense).
    # Actually, it's simpler: for a chain like v1, v2, v3, v4 where v(i+1) = v(i)*k,
    # we cannot pick both v1 and v2, v2 and v3, v3 and v4.
    # This is equivalent to finding the maximum independent set on a path graph, which is ceil(length/2) if we start from one end?
    # No, for a path of length L (nodes), the max independent set size is ceil(L/2)?
    # Let's check:
    # Length 1: {v1} -> size 1. ceil(1/2)=1.
    # Length 2: {v1, v2} -> pick 1. ceil(2/2)=1.
    # Length 3: {v1, v2, v3} -> pick {v1, v3} -> size 2. ceil(3/2)=2.
    # Length 4: {v1, v2, v3, v4} -> pick {v1, v3} or {v1, v4} or {v2, v4} -> size 2. ceil(4/2)=2.
    # So yes, for a chain of length L, we can take ceil(L/2) elements.
    # But wait, is it always optimal to just split into chains and take ceil(L/2)?
    # The conflict is strictly y = x * k. This forms directed edges x -> x*k.
    # Since all numbers are distinct and positive, these form a set of disjoint paths (chains).
    # Example: 2, 4, 8, 16 with k=2. Chain: 2-4-8-16. Length 4. Max independent set size 2 (e.g., {2,8} or {2,16} or {4,16}).
    # Example: 3, 6, 12 with k=2. Chain: 3-6-12. Length 3. Max independent set size 2 ({3,12}).
    # So the strategy is:
    # 1. Identify all chains.
    # 2. For each chain of length L, add ceil(L/2) to the total.

    # How to identify chains efficiently?
    # We can start from numbers that are not divisible by k (in the context of the set) or rather,
    # numbers x such that x/k is NOT in the set. These are the "heads" of the chains.
    # Then we follow x, x*k, x*k^2... until we run out.

    # However, k can be large, so we just multiply.
    # Since n is up to 10^5, we can do this in O(n) or O(n log n).
    
    # Optimization:
    # Sort the array.
    # Use a set for O(1) lookups.
    # Mark visited elements to avoid processing the same chain multiple times.
    
    visited = set()
    total_count = 0
    
    # Sort to help with processing, though not strictly necessary if we iterate all heads
    # But sorting helps if we want to process in order, but the head identification works regardless.
    # Let's iterate through the sorted array to find heads.
    # A number x is a head if x % k != 0 OR (x // k) is not in the set.
    # Actually, since we deal with integers, x/k might not be integer.
    # Condition for head: x is in set AND (x % k != 0 OR (x // k) not in set).
    
    sorted_a = sorted(a)
    
    for x in sorted_a:
        if x in visited:
            continue
        
        # Check if x is a head of a chain
        is_head = False
        if x % k != 0:
            is_head = True
        else:
            prev = x // k
            if prev not in s:
                is_head = True
        
        if is_head:
            current_chain_len = 0
            curr = x
            while curr in s:
                visited.add(curr)
                current_chain_len += 1
                if curr * k in s:
                    curr = curr * k
                else:
                    break
            
            # Add ceil(current_chain_len / 2)
            # ceil(L/2) = (L + 1) // 2 using integer division
            total_count += (current_chain_len + 1) // 2
            
    print(total_count)

if __name__ == '__main__':
    solve()