import sys
from collections import deque, defaultdict

# Increase recursion depth just in case, though we use iterative BFS
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        n = int(next(iterator))
        k = int(next(iterator))
        prefs = []
        for _ in range(n):
            prefs.append(int(next(iterator)))
    except StopIteration:
        return

    # If k is 0, no one can go
    if k == 0:
        print(0)
        return

    # Build the dependency graph
    # We need to find the maximum number of nodes we can select such that
    # if a node is selected, its dependency (pref) is also selected.
    # This is equivalent to finding the maximum weight closure in a graph where
    # every node has weight 1.
    #
    # Algorithm:
    # 1. Identify "root" components: nodes that are not depended upon by anyone else.
    #    Actually, it's easier to think in reverse:
    #    If node A depends on node B (A -> B), then if A is in, B must be in.
    #    We can condense the graph into Strongly Connected Components (SCCs).
    #    Within an SCC, if any node is picked, all nodes in the SCC must be picked.
    #    Then we build a DAG of SCCs.
    #    In the DAG, if an SCC depends on another SCC, the dependency edge exists.
    #    We want to pick a set of SCCs with maximum total size such that dependencies are met.
    #    This is still a closure problem on the DAG.
    #
    #    However, there is a simpler greedy approach for this specific problem structure
    #    (often called the "Bus Problem" or similar):
    #    - Calculate the "in-degree" of each node in the dependency graph (how many people require this person).
    #    - Wait, the condition is: if I pick person i, I MUST pick person prefs[i].
    #    - Let's reverse the thinking:
    #      Consider the graph where edges go from i -> prefs[i].
    #      If we pick a set of nodes, it must be closed under the "must include" relation.
    #      This is exactly the Maximum Weight Closure problem.
    #      Since all weights are 1, we want max nodes.
    #
    #    Standard reduction for Max Weight Closure:
    #    Create a source S and sink T.
    #    For each node i with weight w_i > 0:
    #      Add edge S -> i with capacity w_i.
    #    For each dependency i -> j (i requires j):
    #      Add edge i -> j with capacity infinity.
    #    Max Weight = Sum of all positive weights - Min Cut.
    #    Here, all weights are 1. So Max Weight = n - Min Cut.
    #    The answer is the size of the closure, which is the max weight.
    #
    #    Steps:
    #    1. Build graph: for each i, add edge i -> prefs[i].
    #    2. Build flow network:
    #       Source S=0, Sink T=n+1.
    #       Nodes 1..n.
    #       Edge S -> i with cap 1 for all i.
    #       Edge i -> prefs[i] with cap INF for all i.
    #    3. Compute Max Flow from S to T.
    #    4. Result = n - Max Flow.
    #
    #    Constraints: n <= 1000. Max Flow with Dinic is efficient enough.

    # Build adjacency list for flow network
    # Nodes: 0 (Source), 1..n (Participants), n+1 (Sink)
    source = 0
    sink = n + 1
    capacity = [[0] * (n + 2) for _ in range(n + 2)]
    graph = [[] for _ in range(n + 2)]

    def add_edge(u, v, cap):
        graph[u].append([v, cap, len(graph[v])])
        graph[v].append([u, 0, len(graph[u]) - 1])

    # Edges from Source to each participant with capacity 1
    for i in range(1, n + 1):
        add_edge(source, i, 1)

    # Edges for dependencies: i -> prefs[i] with infinite capacity
    INF = float('inf')
    for i in range(1, n + 1):
        target = prefs[i - 1]  # prefs is 0-indexed in list, but values are 1..n
        # If target is out of range (shouldn't be based on problem statement), skip
        if 1 <= target <= n:
            add_edge(i, target, INF)

    # Dinic's Algorithm
    level = []
    ptr = []

    def bfs():
        nonlocal level
        level = [-1] * (n + 2)
        level[source] = 0
        queue = deque([source])
        while queue:
            u = queue.popleft()
            for v, cap, rev_idx in graph[u]:
                if cap > 0 and level[v] < 0:
                    level[v] = level[u] + 1
                    queue.append(v)
        return level[sink] >= 0

    def dfs(u, pushed):
        if pushed == 0 or u == sink:
            return pushed
        for i in range(ptr[u], len(graph[u])):
            ptr[u] = i  # Update pointer to avoid revisiting edges
            v, cap, rev_idx = graph[u][i]
            if level[v] != level[u] + 1 or cap == 0:
                continue
            tr = dfs(v, min(pushed, cap))
            if tr == 0:
                continue
            # Update residual capacities
            graph[u][i][1] -= tr
            graph[v][rev_idx][1] += tr
            return tr
        return 0

    max_flow = 0
    while bfs():
        ptr = [0] * (n + 2)
        while True:
            pushed = dfs(source, INF)
            if pushed == 0:
                break
            max_flow += pushed

    # The maximum number of participants is total participants - max_flow
    # Because max_flow represents the minimum cut, which equals the minimum number of people
    # we must exclude to satisfy all dependencies.
    result = n - max_flow
    print(result)

if __name__ == "__main__":
    solve()