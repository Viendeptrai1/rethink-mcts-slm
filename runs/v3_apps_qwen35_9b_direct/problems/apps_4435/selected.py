import sys
from collections import deque

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    n = int(next(iterator))
    a = [0] * (n + 1)
    for i in range(1, n + 1):
        a[i] = int(next(iterator))

    # We need to find the minimum moves to reach a node with opposite parity.
    # This is a multi-source BFS problem.
    # Instead of running BFS from each node (which would be O(n^2)),
    # we can run two BFS traversals:
    # 1. Start BFS from all nodes that have EVEN values. Compute dist_even[i] = min moves from i to any even node.
    #    But wait, the problem asks: for each i, min moves to reach a node j with opposite parity.
    #    If a[i] is odd, we need distance to nearest even.
    #    If a[i] is even, we need distance to nearest odd.
    #
    # However, the graph is directed. From i, we can go to i - a[i] or i + a[i].
    # The edges are: i -> (i - a[i]) and i -> (i + a[i]).
    #
    # We want: for each i, min distance to any j such that parity(a[j]) != parity(a[i]).
    #
    # Approach:
    # Let's define two arrays:
    # dist_to_even[i]: min moves from i to reach any node j where a[j] is even.
    # dist_to_odd[i]: min moves from i to reach any node j where a[j] is odd.
    #
    # If we can compute these two arrays efficiently, the answer for i is:
    #   if a[i] is odd: dist_to_even[i]
    #   if a[i] is even: dist_to_odd[i]
    #
    # How to compute dist_to_even?
    # We can reverse the graph!
    # Original edges: u -> v if v = u - a[u] or v = u + a[u].
    # Reversed edges: v -> u if u - a[u] == v or u + a[u] == v.
    #   i.e., u = v + a[u] (but a[u] depends on u, so we need to check both possibilities).
    #   Actually, for a fixed v, which u can jump to v?
    #   Case 1: u - a[u] = v  => u = v + a[u]. This is hard because a[u] is on both sides.
    #   Case 2: u + a[u] = v  => u = v - a[u]. Also hard.
    #
    # Alternative approach: Multi-source BFS on the original graph?
    # No, because the target set depends on the starting node's parity.
    # But notice:
    #   If we want dist_to_even[i], we are looking for the shortest path from i to ANY even node.
    #   This is equivalent to: in the graph, what is the distance from the set of all even nodes to i, 
    #   but traversing edges in REVERSE direction.
    #
    # Let's formalize the reverse graph construction.
    # We want to compute D_even[i] = min distance from i to any node j with a[j] even.
    # This is equal to the distance from the set S_even = {j | a[j] is even} to i in the REVERSE graph.
    #
    # Reverse graph edges:
    # For each node u, it has outgoing edges in original graph to:
    #   v1 = u - a[u] (if valid)
    #   v2 = u + a[u] (if valid)
    # So in reverse graph, v1 has an incoming edge from u, meaning v1 -> u in reverse graph.
    # Similarly, v2 -> u in reverse graph.
    #
    # Algorithm for D_even:
    # 1. Initialize D_even array with infinity, D_odd array with infinity.
    # 2. Create a queue for BFS.
    # 3. For D_even:
    #    - Identify all nodes j where a[j] is even.
    #    - Set D_even[j] = 0 for these nodes.
    #    - Push all such j into the queue.
    #    - Run BFS on the REVERSE graph.
    #    - When expanding node u in reverse BFS, we look for all nodes v such that there is an edge v -> u in original graph.
    #      i.e., v can jump to u.
    #      Condition: v - a[v] == u  OR  v + a[v] == u.
    #      From v - a[v] == u => v = u + a[v]. We don't know a[v] yet? No, a[v] is known from input.
    #      But we don't know v. We need to find v such that v jumps to u.
    #      Possibility 1: v = u + a[v]. This implies a[v] = v - u. Since we know a[v], we can check if a[v] == v - u.
    #        So v must satisfy: v - u = a[v] => v = u + a[v]. This is circular if we try to solve for v directly without iterating.
    #        However, note that v must be in the range [1, n].
    #        Also, from v - a[v] = u, we have v = u + a[v]. Since a[v] >= 1, v > u.
    #        And a[v] = v - u. So for a fixed u, we are looking for v > u such that a[v] = v - u.
    #        This looks like we might need to iterate over possible v? That could be O(n^2).
    #
    # Let's re-evaluate. Is there a way to avoid O(n^2)?
    # Notice the constraints: n <= 2e5. O(n^2) is too slow.
    #
    # Let's reconsider the reverse edge condition.
    # Edge in original: u -> v exists if v = u - a[u] or v = u + a[u].
    # Reverse edge: v -> u exists if u = v + a[u] (from u - a[u] = v) OR u = v - a[u] (from u + a[u] = v).
    #
    # Wait, the condition "u = v + a[u]" involves a[u].
    # But in the reverse BFS, when we are at node v (in reverse graph), we want to find all u such that v -> u is a valid reverse edge.
    # This means in original graph, u -> v was an edge.
    # So u could be:
    #   Type 1: u - a[u] = v  => u = v + a[u]. Here a[u] is the value at u.
    #   Type 2: u + a[u] = v  => u = v - a[u]. Here a[u] is the value at u.
    #
    # This still seems to require knowing u to check a[u].
    # However, observe:
    #   For Type 1: u = v + a[u]. Since a[u] >= 1, u > v.
    #   Also, a[u] = u - v.
    #   So we are looking for u > v such that a[u] == u - v.
    #   This is equivalent to: a[u] + v = u.
    #   Or: u - a[u] = v.
    #
    #   For Type 2: u = v - a[u]. Since a[u] >= 1, u < v.
    #   Also, a[u] = v - u.
    #   So we are looking for u < v such that a[u] == v - u.
    #   This is equivalent to: a[u] + u = v.
    #
    # So, for a fixed v, the predecessors u in the original graph (which become successors in reverse graph) are:
    #   1. u > v such that u - a[u] = v.
    #   2. u < v such that u + a[u] = v.
    #
    # How to efficiently find these u's?
    # We can precompute lists!
    # Let's create two adjacency lists for the reverse graph:
    #   rev_adj_type1[v]: list of u such that u - a[u] = v (i.e., u jumps left to v).
    #   rev_adj_type2[v]: list of u such that u + a[u] = v (i.e., u jumps right to v).
    #
    # Construction:
    #   Iterate u from 1 to n:
    #     val = a[u]
    #     if u - val >= 1:
    #       rev_adj_type1[u - val].append(u)
    #     if u + val <= n:
    #       rev_adj_type2[u + val].append(u)
    #
    # Then the reverse graph for BFS is simply the union of these two lists.
    # From v, we can go to any u in rev_adj_type1[v] OR any u in rev_adj_type2[v].
    #
    # This construction is O(n). The BFS is O(n + edges) = O(n).
    #
    # So the plan:
    # 1. Build reverse adjacency lists:
    #      rev_left[v] = [u | u - a[u] == v]
    #      rev_right[v] = [u | u + a[u] == v]
    # 2. Compute dist_to_even:
    #      Initialize dist_to_even with -1 (or infinity).
    #      Queue Q.
    #      For i in 1..n:
    #        if a[i] % 2 == 0:
    #          dist_to_even[i] = 0
    #          Q.append(i)
    #      While Q not empty:
    #        u = Q.popleft()
    #        For v in rev_left[u]:
    #          if dist_to_even[v] == -1:
    #            dist_to_even[v] = dist_to_even[u] + 1
    #            Q.append(v)
    #        For v in rev_right[u]:
    #          if dist_to_even[v] == -1:
    #            dist_to_even[v] = dist_to_even[u] + 1
    #            Q.append(v)
    # 3. Compute dist_to_odd similarly, starting with all odd nodes as sources (dist=0).
    # 4. For each i:
    #      if a[i] is odd: ans[i] = dist_to_even[i]
    #      else: ans[i] = dist_to_odd[i]
    #      If the distance is still -1, output -1.

    # Implementation details:
    # Use 1-based indexing for convenience to match problem statement, but arrays in Python are 0-based.
    # We'll use size n+1 and ignore index 0.

    # Precompute reverse adjacencies
    rev_left = [[] for _ in range(n + 1)]
    rev_right = [[] for _ in range(n + 1)]

    for u in range(1, n + 1):
        val = a[u]
        left_target = u - val
        if left_target >= 1:
            rev_left[left_target].append(u)
        right_target = u + val
        if right_target <= n:
            rev_right[right_target].append(u)

    # BFS for distance to even
    dist_even = [-1] * (n + 1)
    q = deque()
    for i in range(1, n + 1):
        if a[i] % 2 == 0:
            dist_even[i] = 0
            q.append(i)

    while q:
        u = q.popleft()
        d = dist_even[u]
        
        # Explore reverse edges from u
        for v in rev_left[u]:
            if dist_even[v] == -1:
                dist_even[v] = d + 1
                q.append(v)
        for v in rev_right[u]:
            if dist_even[v] == -1:
                dist_even[v] = d + 1
                q.append(v)

    # BFS for distance to odd
    dist_odd = [-1] * (n + 1)
    q = deque()
    for i in range(1, n + 1):
        if a[i] % 2 != 0:
            dist_odd[i] = 0
            q.append(i)

    while q:
        u = q.popleft()
        d = dist_odd[u]
        
        for v in rev_left[u]:
            if dist_odd[v] == -1:
                dist_odd[v] = d + 1
                q.append(v)
        for v in rev_right[u]:
            if dist_odd[v] == -1:
                dist_odd[v] = d + 1
                q.append(v)

    # Construct result
    res = []
    for i in range(1, n + 1):
        if a[i] % 2 == 1:
            # Need even
            res.append(str(dist_even[i]))
        else:
            # Need odd
            res.append(str(dist_odd[i]))

    print(" ".join(res))

if __name__ == "__main__":
    solve()