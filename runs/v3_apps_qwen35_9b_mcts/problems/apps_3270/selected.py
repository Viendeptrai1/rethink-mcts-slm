import sys
from collections import deque

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
    dictionary = set(words)

    if start == end:
        print("")
        print(0)
        return

    # Helper to generate neighbors
    def get_neighbors(word):
        neighbors = []
        for i in range(len(word)):
            original_char = word[i]
            for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                if c != original_char:
                    new_word = word[:i] + c + word[i+1:]
                    neighbors.append(new_word)
        return neighbors

    # Check if a path exists in the current dictionary
    def bfs_shortest_path(start_node, end_node, word_set):
        if start_node not in word_set or end_node not in word_set:
            return None, float('inf')
        
        queue = deque([(start_node, 0)])
        visited = {start_node: 0}
        
        while queue:
            current, dist = queue.popleft()
            if current == end_node:
                return current, dist
            for neighbor in get_neighbors(current):
                if neighbor in word_set and neighbor not in visited:
                    visited[neighbor] = dist + 1
                    queue.append((neighbor, dist + 1))
        return None, float('inf')

    # Initial BFS to find shortest path and reconstruct it
    # Since we need to find a bridge, we need the actual path, not just distance.
    # However, generating the full path for every candidate might be slow if the graph is large.
    # But N <= 1000 and word length <= 8, so BFS is feasible.
    
    # Let's first check if a path exists without adding any word
    path_exists, _ = bfs_shortest_path(start, end, dictionary)
    
    if not path_exists:
        # No path exists even with the current dictionary.
        # We need to add a word to make it possible.
        # The added word must connect the start component to the end component.
        # It must be a neighbor of some node reachable from start and some node that can reach end.
        # Actually, simpler: try adding a word that is a neighbor of start and a neighbor of end?
        # Or a word that connects two components.
        # Strategy: Find all words reachable from start (component S) and all words that can reach end (component E).
        # If S and E are disjoint, we need a word w such that w is neighbor of some u in S and v in E?
        # No, w must be in the dictionary (virtually). So w must be neighbor of u (in S) and neighbor of v (in E)?
        # Wait, if we add w, the path is ... -> u -> w -> v -> ...
        # So w must be a neighbor of u (where u is in S) and a neighbor of v (where v is in E).
        # But u and v don't have to be the same.
        # However, to minimize steps, we want the shortest path.
        # Let's collect all nodes in the component of start and all nodes in the component of end (reversed graph).
        
        # Component of start
        comp_start = set()
        q = deque([start])
        comp_start.add(start)
        while q:
            u = q.popleft()
            for v in get_neighbors(u):
                if v in dictionary and v not in comp_start:
                    comp_start.add(v)
                    q.append(v)
        
        # Component that can reach end (reverse BFS from end)
        comp_end = set()
        q = deque([end])
        comp_end.add(end)
        while q:
            u = q.popleft()
            for v in get_neighbors(u):
                if v in dictionary and v not in comp_end:
                    comp_end.add(v)
                    q.append(v)
        
        if not comp_start or not comp_end:
            # Should not happen if start/end are in dictionary, but just in case
            print("0")
            print("-1")
            return

        # We need a word w (not in dictionary) such that:
        # 1. w is a neighbor of some u in comp_start
        # 2. w is a neighbor of some v in comp_end
        # 3. w is not in dictionary
        # 4. w is not start or end (though they are in dict, so w won't be them)
        # To minimize total steps: dist(start, u) + 1 + 1 + dist(v, end)
        # We want to minimize dist(start, u) + dist(v, end).
        # Since u is in comp_start, dist(start, u) is known (BFS levels).
        # Since v is in comp_end, dist(v, end) is known (BFS levels from end).
        
        # Precompute distances from start to all nodes in comp_start
        dist_start = {}
        q = deque([start])
        dist_start[start] = 0
        while q:
            u = q.popleft()
            for v in get_neighbors(u):
                if v in dictionary and v not in dist_start:
                    dist_start[v] = dist_start[u] + 1
                    q.append(v)
        
        # Precompute distances from end to all nodes in comp_end (reverse)
        dist_end = {}
        q = deque([end])
        dist_end[end] = 0
        while q:
            u = q.popleft()
            for v in get_neighbors(u):
                if v in dictionary and v not in dist_end:
                    dist_end[v] = dist_end[u] + 1
                    q.append(v)
        
        best_word = None
        min_steps = float('inf')
        
        # Iterate over all possible words that could be the bridge
        # The bridge word w must differ by 1 char from some u in comp_start and some v in comp_end.
        # Instead of iterating all possible words (26^L), iterate over neighbors of comp_start nodes.
        candidates = set()
        for u in comp_start:
            for v in get_neighbors(u):
                if v not in dictionary:
                    candidates.add(v)
        
        # Also consider neighbors of comp_end nodes that are not in dictionary
        for v in comp_end:
            for w in get_neighbors(v):
                if w not in dictionary:
                    candidates.add(w)
        
        # Filter candidates: must be neighbor of at least one in comp_start AND at least one in comp_end
        valid_candidates = []
        for w in candidates:
            is_neighbor_start = False
            is_neighbor_end = False
            for u in comp_start:
                if w in get_neighbors(u):
                    is_neighbor_start = True
                    break
            for v in comp_end:
                if w in get_neighbors(v):
                    is_neighbor_end = True
                    break
            if is_neighbor_start and is_neighbor_end:
                # Calculate path length: dist(start, u) + 1 + 1 + dist(v, end)
                # We need the minimum dist(start, u) + dist(v, end) for this w
                min_u_dist = float('inf')
                min_v_dist = float('inf')
                
                for u in comp_start:
                    if w in get_neighbors(u):
                        if dist_start[u] < min_u_dist:
                            min_u_dist = dist_start[u]
                
                for v in comp_end:
                    if w in get_neighbors(v):
                        if dist_end[v] < min_v_dist:
                            min_v_dist = dist_end[v]
                
                total = min_u_dist + 1 + 1 + min_v_dist
                if total < min_steps:
                    min_steps = total
                    best_word = w
                elif total == min_steps:
                    if best_word is None or w < best_word:
                        best_word = w
        
        if best_word:
            print(best_word)
            print(min_steps)
        else:
            print("0")
            print("-1")
        return

    # If a path exists, we try to shorten it by adding a word.
    # The added word w creates a shortcut.
    # Path: start -> ... -> u -> w -> v -> ... -> end
    # Where u and v are in the original shortest path, and dist(u, v) in original graph is 2 (via w).
    # Actually, u and v might not be adjacent in the original path, but adding w connects them directly.
    # The new path length would be: dist(start, u) + 1 + 1 + dist(v, end).
    # We want to minimize this.
    # Note: u and v must be such that there is no direct edge between them in the original graph (otherwise w doesn't help directly as a shortcut of length 2, unless it's a different route).
    # But actually, if u and v are distance 2 apart in the original graph, adding w makes them distance 2 (u->w->v) which is same as u->x->v.
    # Wait, if u and v are distance 2, say u->x->v, then adding w (where w is neighbor of u and v) gives u->w->v.
    # This doesn't shorten the path unless the original path went through x and x was a bottleneck?
    # No, the problem asks to minimize the number of steps.
    # If the original shortest path has length L, and we add w, the new path might be shorter.
    # The new path uses w. So it looks like: start -> ... -> u -> w -> v -> ... -> end.
    # The length is dist(start, u) + 1 + 1 + dist(v, end).
    # We need to find u and v in the original graph such that:
    # 1. There is a path from start to u.
    # 2. There is a path from v to end.
    # 3. w is a word not in dictionary, w is neighbor of u, w is neighbor of v.
    # 4. The new total length is minimized.
    # 5. Also, we must ensure that the path from start to u and v to end does not use w (which is fine since w is new).
    # 6. And we must ensure that the original path from u to v (if any) is not shorter than 2? 
    #    Actually, if dist(u, v) in original graph is 1, then u->v is 1 step. u->w->v is 2 steps. No gain.
    #    If dist(u, v) in original graph is 2, then u->x->v is 2 steps. u->w->v is 2 steps. No gain.
    #    If dist(u, v) in original graph is > 2, then u->w->v (2 steps) is a shortcut!
    #    So we need to find u, v such that dist(u, v) >= 3 in the original graph, and adding w reduces the distance between u and v to 2.
    #    Then the new total path length = dist(start, u) + 2 + dist(v, end).
    #    We want to minimize this value.
    
    # Step 1: Find the shortest path in the original graph to get baseline and identify nodes.
    # But we don't need the specific path, we need dist(start, u) and dist(v, end) for all u, v.
    # Let's compute dist_start and dist_end for all nodes in the dictionary.
    
    # BFS from start
    dist_start_all = {}
    q = deque([start])
    dist_start_all[start] = 0
    while q:
        u = q.popleft()
        for v in get_neighbors(u):
            if v in dictionary and v not in dist_start_all:
                dist_start_all[v] = dist_start_all[u] + 1
                q.append(v)
    
    # BFS from end (reverse)
    dist_end_all = {}
    q = deque([end])
    dist_end_all[end] = 0
    while q:
        u = q.popleft()
        for v in get_neighbors(u):
            if v in dictionary and v not in dist_end_all:
                dist_end_all[v] = dist_end_all[u] + 1
                q.append(v)
    
    # If start or end not reachable from each other, handled above.
    # Now, iterate over all possible bridge words w.
    # w must be a neighbor of some u in dictionary and some v in dictionary.
    # w must not be in dictionary.
    # We want to minimize: dist_start_all[u] + 2 + dist_end_all[v]
    # Subject to: dist_start_all[u] + dist_end_all[v] + 2 < current_shortest_path_length
    # And: dist(u, v) in original graph > 2 (so that the shortcut is valid and actually shorter).
    # Actually, even if dist(u, v) == 2, if the original shortest path went through a different node x, 
    # and we replace u->x->v with u->w->v, the length is the same. So no improvement.
    # We strictly need improvement.
    
    # First, find the current shortest path length L.
    # We can do this by checking if end is in dist_start_all.
    if end not in dist_start_all:
        # This case was handled before, but just in case
        print("0")
        print("-1")
        return
    
    current_min_len = dist_start_all[end]
    
    best_word = None
    min_new_len = float('inf')
    
    # Generate candidate words w
    # w must be a neighbor of some u in dictionary.
    # To avoid duplicates, we can collect all such w.
    candidates = set()
    for u in dictionary:
        for v in get_neighbors(u):
            if v not in dictionary:
                candidates.add(v)
    
    # Also, w must be a neighbor of some v in dictionary. (Redundant check but good for logic)
    # Actually, if w is neighbor of u, and we use it to connect u and v, then w must be neighbor of v too.
    # So we only care about w that are neighbors of at least two dictionary words?
    # Not necessarily two, but at least one u and one v such that the path goes through them.
    # But if w is only neighbor of one dictionary word, it can't form a bridge between two dictionary words.
    # So w must have degree >= 2 in the graph (dictionary + w).
    
    # Let's filter candidates: w must be neighbor of at least two distinct words in dictionary?
    # Yes, because the path is ... -> u -> w -> v -> ...
    # So w must connect u and v.
    
    # Optimization: Instead of iterating all candidates, iterate all pairs (u, v) that are far apart?
    # No, iterating candidates is better.
    
    for w in candidates:
        # Find best u and v for this w
        # u must be neighbor of w, v must be neighbor of w
        # We want to minimize dist_start_all[u] + dist_end_all[v]
        
        best_u_dist = float('inf')
        best_v_dist = float('inf')
        
        # Check neighbors of w that are in dictionary
        # Since w is not in dictionary, we just check its neighbors in dictionary
        neighbors_in_dict = []
        for char_idx in range(len(w)):
            original = w[char_idx]
            for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                if c != original:
                    candidate_word = w[:char_idx] + c + w[char_idx+1:]
                    if candidate_word in dictionary:
                        neighbors_in_dict.append(candidate_word)
        
        if len(neighbors_in_dict) < 2:
            continue
            
        # Find min dist_start for any neighbor
        for u in neighbors_in_dict:
            if dist_start_all[u] < best_u_dist:
                best_u_dist = dist_start_all[u]
        
        # Find min dist_end for any neighbor
        for v in neighbors_in_dict:
            if dist_end_all[v] < best_v_dist:
                best_v_dist = dist_end_all[v]
        
        # Total new length
        new_len = best_u_dist + 2 + best_v_dist
        
        # Check if this is an improvement
        if new_len < current_min_len:
            min_new_len = new_len
            best_word = w
        elif new_len == current_min_len:
            # We want the lexicographically smallest word
            if best_word is None or w < best_word:
                best_word = w
    
    if best_word:
        print(best_word)
        print(min_new_len)
    else:
        print("0")
        print("-1")

if __name__ == "__main__":
    solve()