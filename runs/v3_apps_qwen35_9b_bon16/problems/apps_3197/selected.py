import sys
from collections import defaultdict

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        n = int(next(iterator))
        k = int(next(iterator))
        preferences = [int(next(iterator)) for _ in range(n)]
    except StopIteration:
        return

    # Count how many people require each specific person
    required_count = [0] * (n + 1)
    for p in preferences:
        required_count[p] += 1

    # Separate people into two groups:
    # 1. Those who are required by at least one other person (self-loop allowed but still counted)
    #    Actually, we need to distinguish between "pure" self-loops and dependencies on others.
    #    A person i is "safe" to include alone if:
    #       - They require themselves (pref[i] == i) AND
    #       - No one else requires them? Not exactly.
    #
    # Let's refine the logic:
    # We want to select a set S of size <= k such that for every i in S, pref[i] is in S.
    #
    # Strategy:
    # 1. Identify "root" nodes that do not depend on anyone else (i.e., pref[i] == i).
    #    Wait, the problem says "unless the x_i-th participant also joins".
    #    If x_i == i, it's a self-loop, which is always satisfied if they join.
    #    If x_i != i, they depend on someone else.
    #
    # However, simply taking all self-loops isn't enough because those others might also have dependencies.
    # But note: if A depends on B, and B depends on A, they form a cycle. Neither can go unless both go.
    # If A depends on B, and B is a self-loop, then A can go if B goes.
    #
    # Better approach:
    # - People who only require themselves (pref[i] == i) can always be included without forcing anyone else.
    #   Let's call this set S_self.
    # - For everyone else (pref[i] != i), they are part of chains or cycles leading to someone.
    #   Ultimately, every dependency chain must end at a self-loop (pref[p] == p) or in a cycle with no exit.
    #   If a chain ends in a cycle with no self-loop, those participants can NEVER be included because there's no root.
    #
    # Algorithm:
    # 1. Mark all nodes that have pref[i] == i as "available roots".
    # 2. Traverse backwards? Or forwards?
    #    If i depends on j (pref[i] == j), and j is available, then i becomes available too.
    #    We can iteratively add people whose dependency is already satisfied.
    #
    # Steps:
    # - Create a boolean array `can_join` initialized to False.
    # - Mark all i where pref[i] == i as `can_join[i] = True`.
    # - Use a queue for nodes whose dependency is satisfied.
    # - While queue is not empty:
    #     pop u.
    #     For all v such that pref[v] == u:
    #         if not can_join[v]:
    #             can_join[v] = True
    #             push v to queue.
    #
    # - Count total people with can_join[i] == True. Let this be `cnt`.
    # - If cnt <= k, answer is cnt.
    # - If cnt > k, we can only take k people. Since all selected people are mutually compatible
    #   (each's dependency is within the set), we can just take any k of them.
    #   Wait, is it always optimal to take the maximum possible compatible set?
    #   Yes, because adding more people never invalidates existing constraints.
    #   The constraint is: if i is in, pref[i] must be in.
    #   Our construction ensures that for every i in our set, pref[i] is also in our set.
    #   So we can pick up to min(cnt, k).
    #
    # Complexity: O(N) using BFS-like propagation.

    can_join = [False] * (n + 1)
    queue = []

    # Identify initial roots (self-requiring)
    for i in range(1, n + 1):
        if preferences[i-1] == i:
            can_join[i] = True
            queue.append(i)

    # Build reverse adjacency list: who requires whom?
    # Actually we need: for a given u, who has pref[v] == u?
    dependents = [[] for _ in range(n + 1)]
    for i in range(n):
        p = preferences[i]
        # i+1 depends on p
        dependents[p].append(i + 1)

    head = 0
    while head < len(queue):
        u = queue[head]
        head += 1

        for v in dependents[u]:
            if can_join[v]:
                continue
            can_join[v] = True
            queue.append(v)

    count = 0
    for i in range(1, n + 1):
        if can_join[i]:
            count += 1

    print(min(count, k))

if __name__ == "__main__":
    solve()