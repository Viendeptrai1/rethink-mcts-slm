import sys
from collections import deque, defaultdict

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        n = int(next(iterator))
    except StopIteration:
        return

    words = []
    for _ in range(n):
        words.append(next(iterator))

    start = words[0]
    end = words[1]

    if start == end:
        print("")
        print(0)
        return

    word_set = set(words)
    if start not in word_set:
        word_set.add(start)
    if end not in word_set:
        word_set.add(end)

    def get_neighbors(w):
        neighbors = []
        for i in range(len(w)):
            for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                if c != w[i]:
                    new_w = w[:i] + c + w[i+1:]
                    if new_w in word_set:
                        neighbors.append(new_w)
        return neighbors

    # BFS to find shortest path from start to end
    def bfs():
        queue = deque([(start, 0)])
        visited = {start}
        while queue:
            curr, dist = queue.popleft()
            if curr == end:
                return dist
            for nb in get_neighbors(curr):
                if nb not in visited:
                    visited.add(nb)
                    queue.append((nb, dist + 1))
        return -1

    initial_dist = bfs()

    if initial_dist != -1:
        print("")
        print(initial_dist)
        return

    # If no path exists, try adding one word
    # We need to find a word 'bridge' such that:
    # 1. bridge is not in word_set
    # 2. There exists a path from start to bridge (length L1)
    # 3. There exists a path from bridge to end (length L2)
    # 4. Total steps = L1 + L2 + 1 (the +1 is for the transition through the new word? 
    #    Actually, the problem says "number of steps". 
    #    Path: start -> ... -> bridge -> ... -> end.
    #    If we add 'bridge', the path becomes: start -> ... -> neighbor_of_bridge -> bridge -> neighbor_of_bridge -> ... -> end.
    #    Wait, the definition of step is changing one letter.
    #    If we add 'bridge', we can go from a neighbor of 'bridge' to 'bridge' and then to another neighbor.
    #    So the path is: start -> ... -> u -> bridge -> v -> ... -> end.
    #    Steps: dist(start, u) + 1 (u->bridge) + 1 (bridge->v) + dist(v, end).
    #    But u and v must be neighbors of bridge.
    #    Actually, simpler: 
    #    Let d1 = shortest distance from start to any neighbor of bridge (in original graph)
    #    Let d2 = shortest distance from any neighbor of bridge to end (in original graph)
    #    Then total steps = d1 + 1 + 1 + d2 = d1 + d2 + 2?
    #    No. The path is: start -> ... -> u -> bridge -> v -> ... -> end.
    #    The number of edges is: dist(start, u) + 1 (u->bridge) + 1 (bridge->v) + dist(v, end).
    #    We want to minimize this.
    #    Note: u and v are neighbors of bridge in the original dictionary.
    #    So we need to find a word 'bridge' (not in dict) such that:
    #      - It has at least one neighbor in dict (to connect from start side)
    #      - It has at least one neighbor in dict (to connect to end side)
    #      - min(dist(start, u) for u in neighbors(bridge)) + 1 + 1 + min(dist(v, end) for v in neighbors(bridge)) is minimized.
    #    Actually, we can run BFS from start to all nodes, and BFS from end to all nodes (reverse graph is same since undirected).
    #    Let dist_start[u] = shortest distance from start to u in original graph.
    #    Let dist_end[u] = shortest distance from end to u in original graph.
    #    If we add 'bridge', the new path length is:
    #      min_{u in neighbors(bridge)} (dist_start[u]) + 1 + 1 + min_{v in neighbors(bridge)} (dist_end[v])
    #    But note: u and v can be the same? Yes, if bridge connects to the same node, then path is start->...->u->bridge->u->...->end? 
    #    That would be a cycle and not optimal. But mathematically it's allowed. However, we want shortest.
    #    Actually, the path is start -> ... -> u -> bridge -> v -> ... -> end.
    #    The cost is dist_start[u] + 1 + 1 + dist_end[v].
    #    We can rewrite as: (dist_start[u] + dist_end[v]) + 2.
    #    We need to minimize this over all possible 'bridge' words and all pairs (u, v) that are neighbors of 'bridge'.
    #    Constraints: n <= 1000, word length <= 8.
    #    Number of possible words is 26^8 which is too big.
    #    However, the optimal 'bridge' must be formed by changing one letter of some existing word in the dictionary?
    #    Not necessarily. But consider: if 'bridge' is not adjacent to any word in the dictionary, it's useless.
    #    So 'bridge' must have at least one neighbor in the dictionary.
    #    Therefore, 'bridge' must be one letter away from some word w in the dictionary.
    #    So we only need to check candidates that are one letter away from words in the dictionary.
    #    How many such candidates? At most n * 26 * L. With n=1000, L=8, that's 208,000. Manageable.
    #    But we must exclude words already in the dictionary.
    #    Also, we must ensure that the candidate 'bridge' is not start or end (though if it is, we wouldn't need to add it, but we already handled the case where a path exists).
    #    Since we are in the case where no path exists, start and end are not connected. Adding start or end won't help unless they are neighbors of each other? 
    #    But if start and end are neighbors, then initial_dist would be 1, so we wouldn't be here.
    #    So we only consider candidates that are not in word_set.

    # Step 1: Compute dist_start for all words in word_set
    dist_start = {}
    queue = deque([start])
    dist_start[start] = 0
    while queue:
        u = queue.popleft()
        for v in get_neighbors(u):
            if v not in dist_start:
                dist_start[v] = dist_start[u] + 1
                queue.append(v)

    # Step 2: Compute dist_end for all words in word_set
    dist_end = {}
    queue = deque([end])
    dist_end[end] = 0
    while queue:
        u = queue.popleft()
        for v in get_neighbors(u):
            if v not in dist_end:
                dist_end[v] = dist_end[u] + 1
                queue.append(v)

    # If either start or end is unreachable in the original graph, then we definitely need a bridge.
    # But we already know there's no path, so at least one of them might be unreachable from the other.
    # Actually, if start is not connected to any neighbor, then dist_start will only have start.
    # Similarly for end.

    # Generate candidate words
    candidates = set()
    for w in word_set:
        for i in range(len(w)):
            for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                if c != w[i]:
                    new_w = w[:i] + c + w[i+1:]
                    if new_w not in word_set:
                        candidates.add(new_w)

    best_word = None
    best_steps = float('inf')

    for cand in candidates:
        # Check if cand can connect to the graph
        # We need at least one neighbor in word_set for the start side and one for the end side.
        # Actually, we need to form a path: start -> ... -> u -> cand -> v -> ... -> end
        # where u and v are in word_set and are neighbors of cand.
        # Note: u and v can be the same? If u == v, then path is start->...->u->cand->u->...->end.
        # This is valid but likely not optimal. But we take min.
        
        # Find min dist from start to any neighbor of cand
        min_d1 = float('inf')
        for i in range(len(cand)):
            for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                if c != cand[i]:
                    neighbor = cand[:i] + c + cand[i+1:]
                    if neighbor in word_set:
                        if neighbor in dist_start:
                            min_d1 = min(min_d1, dist_start[neighbor])
        
        if min_d1 == float('inf'):
            continue # Cannot reach cand from start

        # Find min dist from any neighbor of cand to end
        min_d2 = float('inf')
        for i in range(len(cand)):
            for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                if c != cand[i]:
                    neighbor = cand[:i] + c + cand[i+1:]
                    if neighbor in word_set:
                        if neighbor in dist_end:
                            min_d2 = min(min_d2, dist_end[neighbor])
        
        if min_d2 == float('inf'):
            continue # Cannot reach end from cand

        total_steps = min_d1 + 1 + 1 + min_d2
        if total_steps < best_steps:
            best_steps = total_steps
            best_word = cand
        elif total_steps == best_steps:
            if best_word is None or cand < best_word:
                best_word = cand

    if best_word is None:
        print("0")
        print("-1")
    else:
        print(best_word)
        print(best_steps)

if __name__ == "__main__":
    solve()