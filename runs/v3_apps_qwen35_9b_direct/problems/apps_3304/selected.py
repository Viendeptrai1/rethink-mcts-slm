import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    iterator = iter(data)
    
    try:
        N = int(next(iterator))
        A = [int(next(iterator)) for _ in range(N)]
        P = [int(next(iterator)) for _ in range(N)]
        V = [int(next(iterator)) for _ in range(N)]
    except StopIteration:
        return

    # Map dwarf index (1-based) to its strength
    dwarf_strength = [0] * (N + 1)
    for i in range(N):
        dwarf_strength[A[i]] = P[i]

    # We need to determine the order of elves to maximize victories.
    # This is a greedy problem.
    # Key Insight:
    # Consider the elves as items that need to be placed into slots (dwarves).
    # Each elf k has a preferred slot A[k]. If occupied, it goes to the next available clockwise.
    # The "next available" logic implies that if we process elves in a certain order,
    # an elf might "jump over" some dwarves that are already taken.
    #
    # However, the critical observation for this specific problem (often found in competitive programming)
    # is related to the structure of the "next available" pointers.
    # Let's define a directed graph where an edge exists from u to v if u is the preferred spot for some elf,
    # and v is the next available spot after u is taken? No, that's dynamic.
    #
    # Alternative approach (Standard solution for this problem):
    # 1. Identify the "chains" of dwarves.
    #    Actually, the problem can be modeled by considering the elves' preferences.
    #    If we sort the elves by their strength, does it help? Not directly because the placement depends on the order.
    #
    # Let's re-evaluate the placement mechanism.
    # "The next elf can enter... only after the one before him found a place to sit."
    # "Elf k approaches A_k. If free, sit. Else, walk clockwise until free."
    #
    # This means the final configuration depends entirely on the permutation of elves.
    # We want to choose a permutation to maximize wins.
    #
    # Consider the dwarves as nodes in a circle. Some dwarves are "preferred" by elves.
    # Specifically, dwarf i is preferred by elf k if A[k] == i.
    # Note: Multiple elves can prefer the same dwarf.
    #
    # Let's analyze the "flow". If we have a set of elves targeting a specific dwarf, and that dwarf is taken,
    # they spill over to the next.
    #
    # There is a known greedy strategy for this problem:
    # 1. Group elves by their preferred dwarf.
    # 2. For each dwarf, we have a list of elves who want to sit there.
    # 3. The "spillover" creates chains.
    #
    # Let's try a different perspective: Reverse the process or use a specific sorting order.
    # Actually, the optimal strategy is to process elves in decreasing order of their strength?
    # Or increasing?
    #
    # Let's look at the constraints and the nature of the "next available".
    # If we place the strongest elves first, they get their best possible spots (closest to preference).
    # If we place weak elves first, they might take spots that strong elves would have wanted, but since strong elves
    # can jump further, maybe it doesn't matter?
    #
    # Wait, if a strong elf is placed first, it takes its preferred spot (if free).
    # If a weak elf is placed first, it takes its preferred spot. Then the strong elf comes, finds it taken, and jumps.
    # The strong elf jumping further might land on a spot where it wins, or loses.
    #
    # Hypothesis: Sort elves by strength descending. Place them one by one.
    # Why? Because a stronger elf has a better chance of winning. We want to give it the "best" available spot.
    # What is the "best" spot for an elf? The one closest to its preference A_k (clockwise distance 0, then 1, etc.).
    # By placing stronger elves first, we ensure they get the closest available spots.
    # If we placed a weak elf first, it might take a spot that is very close to a strong elf's preference, forcing the strong elf
    # to jump further away. Since the strong elf is stronger, it should ideally fight the dwarf closest to its preference
    # (or at least, we want to maximize the number of wins, not necessarily the margin, but the set of opponents matters).
    #
    # Actually, the opponent's strength is fixed for a given dwarf.
    # Elf k fights Dwarf A[k] (or the one it lands on).
    # Win condition: V[k] > P[landed_dwarf].
    #
    # Let's reconsider the "chains".
    # The structure of available seats is dynamic.
    # However, there is a specific property: The relative order of elves in the "spillover" chains matters.
    #
    # Let's try the Greedy approach: Sort elves by strength descending.
    # Simulate the process:
    #   Maintain a set of available dwarf indices.
    #   For each elf (strongest to weakest):
    #     Find the first available dwarf starting from A[k] clockwise.
    #     Assign elf to that dwarf.
    #     Check if V[k] > P[dwarf]. If yes, count win.
    #     Remove dwarf from available set.
    #
    # Is this correct?
    # Counter-example check:
    # Suppose we have 2 elves, 2 dwarves.
    # Elf 1: Pref 1, Strength 10. Dwarf 1: Str 5. Dwarf 2: Str 100.
    # Elf 2: Pref 1, Strength 2.
    #
    # Order 1 (Strong first):
    #   Elf 1 takes Dwarf 1 (10 > 5 -> Win). Dwarf 1 taken.
    #   Elf 2 takes Dwarf 2 (2 < 100 -> Loss).
    #   Total wins: 1.
    #
    # Order 2 (Weak first):
    #   Elf 2 takes Dwarf 1 (2 < 5 -> Loss). Dwarf 1 taken.
    #   Elf 1 takes Dwarf 2 (10 < 100 -> Loss).
    #   Total wins: 0.
    #
    # Here Strong First is better.
    #
    # Another case:
    # Elf 1: Pref 1, Str 10. Dwarf 1: Str 100. Dwarf 2: Str 5.
    # Elf 2: Pref 1, Str 20.
    #
    # Order Strong First (Elf 2 then Elf 1):
    #   Elf 2 takes Dwarf 1 (20 < 100 -> Loss).
    #   Elf 1 takes Dwarf 2 (10 > 5 -> Win).
    #   Total: 1.
    #
    # Order Weak First (Elf 1 then Elf 2):
    #   Elf 1 takes Dwarf 1 (10 < 100 -> Loss).
    #   Elf 2 takes Dwarf 2 (20 > 5 -> Win).
    #   Total: 1.
    #
    # It seems sorting by strength descending is a robust heuristic.
    # Is it provably optimal?
    # The problem is equivalent to: We have a set of tasks (elves) and resources (dwarves).
    # Each task has a preferred resource. If taken, it takes the next available.
    # We want to maximize matches where Value(Task) > Value(Resource).
    #
    # This is a known problem. The optimal strategy is indeed to process elves in decreasing order of strength.
    # Reasoning: A stronger elf can win against a wider range of dwarves. By placing it first, we give it the "closest" available option.
    # If we place a weaker elf first, it might consume a "good" spot (one the strong elf could have won against) or force the strong elf
    # to a "bad" spot. Since the strong elf has a higher threshold to win, it is more valuable to secure a win for it if possible.
    # Specifically, if a strong elf can win against a dwarf, we want to ensure it gets that dwarf (or another it can beat).
    # By taking the closest available, we minimize the "cost" in terms of distance, but more importantly, we reserve the "easy" wins for the strong ones.
    #
    # Implementation details:
    # N up to 5*10^5. O(N^2) simulation is too slow.
    # We need an efficient way to find the next available dwarf clockwise.
    # We can use a Disjoint Set Union (DSU) or a Segment Tree / Ordered Set.
    # DSU approach:
    #   Initially, each dwarf is its own set, pointing to itself.
    #   When a dwarf is taken, we union it with the next dwarf (clockwise).
    #   The representative of the set containing index i will point to the next available dwarf >= i.
    #   Since it's a circle, we need to handle wrap-around.
    #   We can map the circle to a linear array of size 2N to handle wrap-around easily, or just handle the wrap in the DSU logic.
    #   Mapping to 2N:
    #     Dwarves 1..N.
    #     Create nodes 1..2N.
    #     Node i represents dwarf i. Node i+N represents dwarf i (copy for wrap).
    #     Actually, simpler: Just use 1..N, but when looking for next, if we go past N, we wrap to 1.
    #     DSU `find(i)` returns the next available dwarf >= i.
    #     If `find(i)` > N, then we wrap to `find(1)`.
    #     Wait, standard DSU for "next available" works like this:
    #       parent[i] = i initially.
    #       When i is taken, parent[i] = find(i+1).
    #       So find(i) gives the next available.
    #       If find(i) > N, we need to handle the wrap.
    #       We can check if find(i) > N. If so, the next available is find(1).
    #       But wait, if 1 is also taken, find(1) will return something > 1.
    #       So the logic:
    #         idx = find(A[k])
    #         if idx > N: idx = find(1)
    #         assign elf to idx.
    #         union(idx, idx+1) -> parent[idx] = find(idx+1).
    #
    #   Complexity: O(N * alpha(N)). This is efficient enough.
    #
    # Steps:
    # 1. Read input.
    # 2. Store elves as tuples (strength, preferred_dwarf_index).
    # 3. Sort elves by strength descending.
    # 4. Initialize DSU for 1..N+1 (where N+1 is a sentinel or just handle bounds).
    #    Actually, to make it clean, let's use size N+2.
    #    Indices 1 to N are dwarves.
    #    parent[i] = i.
    #    find(i) with path compression.
    # 5. Iterate through sorted elves:
    #    target = A[elf_idx]
    #    pos = find(target)
    #    if pos > N:
    #        pos = find(1)
    #    # Now pos is the dwarf index (1-based)
    #    Check win: V[elf_idx] > P[pos-1] (since P is 0-indexed in list, but dwarf labels are 1-based)
    #    If win, increment count.
    #    # Mark pos as taken: union(pos, pos+1)
    #    parent[pos] = find(pos+1)
    #
    # Note on DSU implementation:
    #   We need an array `parent` of size N+2.
    #   find(i): if parent[i] == i return i else parent[i] = find(parent[i]) return parent[i].
    #   When taking pos, we set parent[pos] = find(pos+1).
    #   This effectively links pos to the next available.
    #   The sentinel N+1 can point to itself or N+2?
    #   If we reach N+1, it means all 1..N are taken? But we have N elves and N dwarves, so exactly one per dwarf.
    #   So we will never query a state where all are taken before the last elf.
    #   However, during the process, if we start at N and it's taken, we go to N+1.
    #   Then we wrap to find(1).
    #   So if find(target) > N, we do find(1).
    #   We need to ensure find(1) works correctly even if 1 is taken.
    #   Yes, if 1 is taken, parent[1] points to something else.
    #
    # One edge case: What if find(1) returns N+1? That implies all dwarves 1..N are taken.
    # But we only place N elves total. So the last elf will find the last available spot.
    # The logic holds.

    # Data structures
    # P is 0-indexed list of strengths for dwarves 1..N.
    # V is 0-indexed list of strengths for elves.
    # A is 0-indexed list of preferences (values 1..N).

    # Sorting elves
    # We need to keep track of original indices to access V correctly?
    # The input gives V in order 1..N corresponding to elves 1..N.
    # A[i] corresponds to elf i+1.
    # So we can create a list of (strength, preferred_dwarf) for each elf.
    # Then sort this list.
    # When processing, we need the elf's strength (for comparison) and the dwarf's strength (from P).
    # We don't need the elf's original index for the logic, just its strength and preference.
    # Wait, the problem says "Elf labeled k". The input V is given for k=1..N.
    # So V[i] is strength of elf i+1.
    # A[i] is preference of elf i+1.
    # So we can just pair them up.

    elves = []
    for i in range(N):
        elves.append((V[i], A[i]))
    
    # Sort descending by strength
    elves.sort(key=lambda x: x[0], reverse=True)

    # DSU initialization
    parent = list(range(N + 2))
    
    def find(i):
        path = []
        while parent[i] != i:
            path.append(i)
            i = parent[i]
        for node in path:
            parent[node] = i
        return i

    # To optimize find, we can use recursion with sys.setrecursionlimit, but iterative is safer.
    # The iterative version above is fine.
    
    wins = 0
    for strength, pref in elves:
        # Find next available starting from pref
        curr = find(pref)
        if curr > N:
            curr = find(1)
        
        # curr is the dwarf index (1-based)
        # Dwarf strength is P[curr-1]
        dwarf_str = P[curr-1]
        
        if strength > dwarf_str:
            wins += 1
        
        # Mark curr as taken
        # Union curr with curr+1
        # We set parent[curr] = find(curr+1)
        # Note: curr+1 can be N+1.
        next_avail = find(curr + 1)
        parent[curr] = next_avail

    print(wins)

if __name__ == '__main__':
    solve()