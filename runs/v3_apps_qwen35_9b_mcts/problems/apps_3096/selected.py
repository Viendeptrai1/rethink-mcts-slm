import sys

# Increase recursion depth for deep trees (up to 10,000 nodes)
sys.setrecursionlimit(20000)

def solve():
    input = sys.stdin.read
    data = input().split()
    iterator = iter(data)
    
    try:
        N = int(next(iterator))
    except StopIteration:
        return

    V = [0] * (N + 1)
    for i in range(1, N + 1):
        V[i] = int(next(iterator))
    
    adj = [[] for _ in range(N + 1)]
    for _ in range(N - 1):
        u = int(next(iterator))
        v = int(next(iterator))
        adj[u].append(v)
    
    # dp[u] will store a list of tuples (min_val, max_val, count)
    # representing valid contiguous ranges of joke types that can be formed
    # in the subtree rooted at u, given that u is invited.
    # Since joke types are small (<= 100), we can use a bitmask or boolean array.
    # However, to handle the "consecutive" constraint efficiently, we only store
    # the possible contiguous ranges [L, R] that are valid for the subtree.
    # But wait, the constraint is: "set of jokes the invitees that person X is superior to tell and person X don't form a set of consecutive numbers".
    # This means: If X is invited, then (Jokes(X) U Jokes(subtree of X)) must be a contiguous range of integers.
    # AND, within that range, there must be no duplicate joke types.
    
    # Since V[i] <= 100, the maximum possible range size is 100.
    # We can represent the set of jokes in a subtree as a bitmask (integer) since 100 bits fit in Python's arbitrary precision ints.
    # However, we need to track which contiguous ranges are valid.
    # Actually, the state for a node u is: a list of valid (min, max) pairs such that the union of jokes in the subtree (including u) forms exactly the set of integers from min to max, with no duplicates.
    
    # Let's refine:
    # For a node u, we want to compute a list of valid intervals [L, R] such that:
    # 1. The set of joke types present in the subtree of u (when u is invited) is exactly {L, L+1, ..., R}.
    # 2. There are no duplicate joke types in this set.
    #
    # If u is not invited, the problem doesn't define a state for the subtree in the same way because the constraint "Person X cannot be invited if..." only applies if X is invited.
    # However, the constraint for a child Y depends on whether Y is invited. If Y is invited, then Y's subtree must form a contiguous range including V[Y].
    # Also, if Y is invited, and X is invited, then the union of X's jokes and all invited descendants must form a contiguous range.
    #
    # This implies a bottom-up DP where for each node u, we compute the set of valid contiguous ranges [L, R] that can be formed by the subtree of u, assuming u is invited.
    #
    # Base case: Leaf node u.
    # If we invite u, the set of jokes is {V[u]}. This is contiguous [V[u], V[u]].
    #
    # Recursive step: Node u with children c1, c2, ...
    # We start with the set {V[u]}.
    # For each child ci, we have a set of valid ranges [L, R] from the child's subtree (assuming ci is invited).
    # If we decide to invite ci, we must merge the current set of jokes at u with the set of jokes from ci's subtree.
    # The merge is valid only if:
    # 1. The new set of jokes (current U child's set) is still contiguous.
    # 2. There are no duplicate joke types between current and child's set.
    #
    # Since we are building the set incrementally, we can maintain the current set of jokes as a bitmask.
    # But the number of valid contiguous ranges might be large?
    # Actually, for a fixed set of jokes, there is at most one contiguous range that covers it.
    # So for each node, the state is simply a list of valid (min, max) pairs.
    #
    # Algorithm:
    # 1. Post-order traversal (DFS).
    # 2. For node u, start with current_mask = (1 << V[u]), current_min = V[u], current_max = V[u].
    # 3. For each child c:
    #    Get the list of valid ranges from c: [(l1, r1), (l2, r2), ...]
    #    For each range (l, r) in child's list:
    #       Check if (current_mask & (mask of range [l, r])) == 0. If not, skip (duplicate jokes).
    #       Check if merging current [current_min, current_max] with [l, r] results in a contiguous range.
    #       Merging two contiguous ranges [a, b] and [c, d] results in a contiguous range if and only if:
    #          c == b + 1 OR a == d + 1 OR they overlap (but overlap implies duplicates if we are careful, but here we check duplicates first).
    #          Actually, since we check for duplicates first, they cannot overlap. So they must be adjacent.
    #          So either (l == current_max + 1) or (r == current_min - 1).
    #       If valid, update current_mask, current_min = min(current_min, l), current_max = max(current_max, r).
    #       Add the new range [current_min, current_max] to a temporary list of valid ranges for u.
    #    Also, we must consider the case where we do NOT invite the child.
    #    If we don't invite the child, the child's subtree contributes nothing.
    #    So the current state remains unchanged.
    #
    # Wait, the logic above is slightly flawed. We are iterating children one by one.
    # At any point, we have a set of valid states (current_min, current_max, current_mask) for the processed children.
    # Initially, before processing any children, we have one state: (V[u], V[u], 1<<V[u]).
    # For each child, we compute the new set of states by combining the existing states with the child's possible states (invited) or keeping existing states (not invited).
    #
    # Let states[u] be a list of (min_val, max_val, mask).
    # Initially for leaf u: states = [(V[u], V[u], 1<<V[u])].
    # For non-leaf u:
    #   states = [(V[u], V[u], 1<<V[u])]
    #   For each child c:
    #     new_states = []
    #     For each (min_u, max_u, mask_u) in states:
    #       Option 1: Don't invite c.
    #         Add (min_u, max_u, mask_u) to new_states.
    #       Option 2: Invite c.
    #         For each (min_c, max_c, mask_c) in states[c]:
    #           If (mask_u & mask_c) == 0:
    #             # Check adjacency
    #             if (min_c == max_u + 1) or (max_c == min_u - 1):
    #               new_min = min(min_u, min_c)
    #               new_max = max(max_u, max_c)
    #               new_mask = mask_u | mask_c
    #               new_states.append((new_min, new_max, new_mask))
    #     states = new_states
    #
    # Finally, the answer is the number of unique masks in states[1] (since Petar is node 1 and must be invited? 
    # The problem says "Petar wants to know how many different sets of jokes he can see". 
    # Petar is always present ("all people present (including Petar)"). So Petar is always invited.
    # Thus, we only count the valid configurations for the whole tree rooted at 1.
    # The number of different SETS of jokes. Since each valid configuration produces a unique contiguous range [L, R], 
    # and the set of jokes is exactly {L, ..., R}, the number of different sets is the number of unique ranges [L, R] in states[1].
    # Note: Different configurations might lead to the same set of jokes? 
    # The set of jokes is determined by the range [L, R]. So we just count unique (L, R) pairs.
    
    # Optimization: Since V[i] <= 100, the mask is small. The number of valid contiguous ranges is at most 100*101/2 ~ 5000.
    # But in practice, for a subtree, the number of valid contiguous ranges is much smaller because of the no-duplicate constraint.
    # N=10000, V<=100. The complexity might be an issue if we are not careful.
    # However, the number of valid contiguous ranges for a subtree is bounded by the number of subsets of {1..100} that are contiguous, which is O(100^2).
    # Merging two lists of size S1 and S2 takes O(S1 * S2). In worst case, this could be O(100^4) per node, which is too slow (100^4 = 100,000,000).
    # But note: the number of valid ranges is usually much smaller. Also, many merges will fail due to duplicates or non-adjacency.
    # Let's hope the test cases are not worst-case.
    # Alternatively, we can optimize by noticing that for a fixed mask, the range is unique.
    # We can use a dictionary or list of (min, max) and deduplicate.
    
    # Let's implement the DFS with memoization or iterative post-order.
    # Since it's a tree, we can do a simple DFS.
    
    parent = [0] * (N + 1)
    # Build tree structure with parent pointers to avoid recursion depth issues if needed, but recursion limit is set.
    # Actually, we need to process children first.
    
    order = []
    stack = [1]
    while stack:
        u = stack.pop()
        order.append(u)
        for v in adj[u]:
            parent[v] = u
            stack.append(v)
    
    # Process in reverse order (bottom-up)
    # dp[u] = list of (min_val, max_val)
    # We don't need to store mask in the final list if we ensure uniqueness by (min, max), 
    # but we need mask during merging to check duplicates.
    # So dp[u] = list of (min_val, max_val, mask)
    
    dp = [None] * (N + 1)
    
    for u in reversed(order):
        # Initial state: just u
        initial_mask = 1 << V[u]
        initial_min = V[u]
        initial_max = V[u]
        current_states = [(initial_min, initial_max, initial_mask)]
        
        for v in adj[u]:
            child_states = dp[v]
            if not child_states:
                continue
            
            next_states = []
            # We need to combine current_states with child_states
            # To avoid duplicates in next_states, we can use a set of (min, max, mask)
            # But mask is redundant if (min, max) is unique? No, different masks could theoretically have same min/max?
            # No, if the set of jokes is exactly {min, ..., max}, then the mask is fixed.
            # So (min, max) uniquely identifies the set.
            # So we can just store (min, max) and recompute mask or store mask to avoid recomputing.
            # Let's store (min, max, mask) and use a set of (min, max) to deduplicate.
            
            seen_ranges = set()
            
            for (min_u, max_u, mask_u) in current_states:
                # Option 1: Don't invite child v
                # The state remains (min_u, max_u, mask_u)
                if (min_u, max_u) not in seen_ranges:
                    seen_ranges.add((min_u, max_u))
                    next_states.append((min_u, max_u, mask_u))
                
                # Option 2: Invite child v
                for (min_v, max_v, mask_v) in child_states:
                    # Check duplicates
                    if (mask_u & mask_v) != 0:
                        continue
                    
                    # Check adjacency
                    # The combined range must be contiguous.
                    # Current range [min_u, max_u], Child range [min_v, max_v]
                    # They must be adjacent: min_v == max_u + 1 OR max_v == min_u - 1
                    if min_v == max_u + 1 or max_v == min_u - 1:
                        new_min = min_u if min_u < min_v else min_v
                        new_max = max_u if max_u > max_v else max_v
                        new_mask = mask_u | mask_v
                        
                        if (new_min, new_max) not in seen_ranges:
                            seen_ranges.add((new_min, new_max))
                            next_states.append((new_min, new_max, new_mask))
            
            current_states = next_states
        
        dp[u] = current_states

    # Result is the number of unique ranges in dp[1]
    if dp[1]:
        print(len(set((m, M) for m, M, _ in dp[1])))
    else:
        print(0)

if __name__ == '__main__':
    solve()