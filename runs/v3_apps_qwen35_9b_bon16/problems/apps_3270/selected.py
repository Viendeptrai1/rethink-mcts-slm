import sys

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
        # Already there, 0 steps. But we need to add a word? 
        # The problem says "what ONE single word could you add... to minimize".
        # If start == end, steps = 0. Adding a word won't make it negative.
        # However, the examples imply we are looking for a path. 
        # If start == end, technically 0 steps. But usually in these problems, 
        # if start==end, we output the word itself or 0 steps. 
        # Let's assume we don't need to add a word if already connected (distance 0).
        # But the output format requires a word. 
        # Re-reading: "If it is possible that there's no word you can add that will that will make your path any shorter... output 0 as the word."
        # If distance is already 0, it can't be shorter. So output 0 and 0? 
        # But the example output for impossible is 0 and -1.
        # Let's assume standard BFS distance.
        print(start)
        print(0)
        return

    word_set = set(words)
    length = len(start)
    
    # Precompute neighbors for all words in dictionary
    # We also need to consider potential new words.
    # A new word must be:
    # 1. Length = word length
    # 2. Not in original dictionary
    # 3. Valid (capital letters only, though input guarantees this)
    
    # Strategy:
    # 1. Check if start and end are already connected in the original graph.
    #    If yes, distance d. Can we reduce d by adding one word?
    #    To reduce distance, we must create a shortcut.
    #    The shortest path using 1 new word w would be:
    #    start -> ... -> w -> ... -> end
    #    Specifically, start -> u -> w -> v -> end where u is neighbor of start, v is neighbor of end, 
    #    and w differs from u by 1 char, w differs from v by 1 char.
    #    Actually, the new word w connects two existing words u and v in the dictionary such that
    #    dist(start, u) + 1 + 1 + dist(v, end) < current_dist(start, end).
    #    Wait, the new word w itself is a step.
    #    Path: start -> ... -> u -> w -> v -> ... -> end
    #    Steps: dist(start, u) + 1 (u->w) + 1 (w->v) + dist(v, end).
    #    We want to minimize this sum.
    #    Note: u could be start, v could be end.
    
    # Let's compute BFS distances from start to all words in dictionary.
    # And BFS distances from end to all words in dictionary (reverse graph is same since undirected).
    
    from collections import deque
    
    def bfs_distances(start_word, graph_words, word_set):
        dist = {w: -1 for w in graph_words}
        dist[start_word] = 0
        q = deque([start_word])
        
        while q:
            curr = q.popleft()
            d = dist[curr]
            # Generate neighbors
            for i in range(length):
                for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                    if c == curr[i]:
                        continue
                    nxt = curr[:i] + c + curr[i+1:]
                    if nxt in word_set and dist[nxt] == -1:
                        dist[nxt] = d + 1
                        q.append(nxt)
        return dist

    # Check original connectivity
    dist_from_start = bfs_distances(start, words, word_set)
    dist_from_end = bfs_distances(end, words, word_set)
    
    if end not in dist_from_start or dist_from_start[end] == -1:
        # Not connected at all
        # We need to find a word w such that path exists.
        # Path: start -> u -> w -> v -> end
        # Where u is neighbor of start (or start itself if length allows direct step? No, step is changing 1 char)
        # u must be in word_set or u is start (if start is not in word_set? But start is in word_set).
        # Actually, the path is: start -> ... -> u -> w -> v -> ... -> end
        # u must be a word reachable from start. v must be a word from which end is reachable.
        # w is the new word.
        # Conditions:
        # w differs from u by 1 char.
        # w differs from v by 1 char.
        # w not in word_set.
        # Total steps = dist_from_start[u] + 1 + 1 + dist_from_end[v]
        # We want to minimize this.
        # If no such u, v, w exist, then impossible.
        
        min_steps = float('inf')
        best_word = None
        
        # Candidates for u: all words in word_set that are reachable from start, plus 'start' itself?
        # Yes, u can be 'start'.
        # Candidates for v: all words in word_set that can reach end, plus 'end' itself.
        
        reachable_u = {start}
        for w in words:
            if dist_from_start[w] != -1:
                reachable_u.add(w)
        
        reachable_v = {end}
        for w in words:
            if dist_from_end[w] != -1:
                reachable_v.add(w)
        
        # Iterate over all possible pairs (u, v)
        for u in reachable_u:
            for v in reachable_v:
                # Check if a bridge word w exists
                # w must differ from u by 1 char and from v by 1 char.
                # We can iterate over all positions and characters for w based on u.
                # Then check if that w is 1 char away from v.
                
                # Optimization: Instead of generating all 26^L words, generate candidates from u.
                candidates = []
                for i in range(length):
                    for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                        if c == u[i]:
                            continue
                        w = u[:i] + c + u[i+1:]
                        # Check if this w is 1 char away from v
                        diff_count = sum(1 for k in range(length) if w[k] != v[k])
                        if diff_count == 1:
                            candidates.append(w)
                
                # Also, u could be equal to v? If u==v, then dist(u,v)=0.
                # Then we need w such that w is 1 from u and 1 from v (same). Impossible unless u!=v.
                # Wait, if u==v, then path is start->...->u->w->u->...->end? That's a loop, not optimal.
                # Unless the shortcut is just start->w->end directly?
                # In that case u=start, v=end. w differs from start by 1, w differs from end by 1.
                # This is covered by the loop if u=start and v=end.
                
                if not candidates:
                    continue
                
                for w in candidates:
                    if w in word_set:
                        continue # Must be a new word
                    
                    # Calculate steps
                    d_u = dist_from_start.get(u, float('inf'))
                    d_v = dist_from_end.get(v, float('inf'))
                    
                    if d_u == float('inf') or d_v == float('inf'):
                        continue
                    
                    total_steps = d_u + 2 + d_v
                    if total_steps < min_steps:
                        min_steps = total_steps
                        best_word = w
                    elif total_steps == min_steps:
                        if best_word is None or w < best_word:
                            best_word = w
        
        if best_word is None:
            print(0)
            print(-1)
        else:
            print(best_word)
            print(min_steps)
        return

    # If originally connected
    original_dist = dist_from_start[end]
    min_steps = original_dist
    best_word = "0" # Placeholder for "no change needed" logic, but we must output a word or 0.
    # If no new word improves it, output 0 and original_dist.
    # Wait, the problem says: "If it is possible that there's no word you can add that will that will make your path any shorter... output 0 (zero) as the word."
    # So if original_dist is minimal, we output 0 and original_dist.
    
    # Now try to improve
    reachable_u = {start}
    for w in words:
        if dist_from_start[w] != -1:
            reachable_u.add(w)
    
    reachable_v = {end}
    for w in words:
        if dist_from_end[w] != -1:
            reachable_v.add(w)
    
    improved = False
    
    for u in reachable_u:
        for v in reachable_v:
            candidates = []
            for i in range(length):
                for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                    if c == u[i]:
                        continue
                    w = u[:i] + c + u[i+1:]
                    diff_count = sum(1 for k in range(length) if w[k] != v[k])
                    if diff_count == 1:
                        candidates.append(w)
            
            for w in candidates:
                if w in word_set:
                    continue
                
                d_u = dist_from_start[u]
                d_v = dist_from_end[v]
                
                # Path: start -> ... -> u -> w -> v -> ... -> end
                # Steps: d_u + 1 + 1 + d_v
                new_steps = d_u + 2 + d_v
                
                if new_steps < min_steps:
                    min_steps = new_steps
                    best_word = w
                    improved = True
                elif new_steps == min_steps:
                    if best_word == "0" or w < best_word:
                        best_word = w
                        improved = True # Technically same length, but we found a word to add. 
                        # But if we already have a solution with 0 (meaning no word added), 
                        # and now we find a word that gives SAME length, do we prefer adding a word?
                        # The problem says: "minimize the number of steps". If equal, then "output the solution word that comes first alphabetically".
                        # "0" is not a word. The output for "no word" is "0".
                        # If we can achieve the same minimum steps by adding a word, is that better?
                        # "If it is possible that there's no word you can add that will that will make your path any shorter... output 0"
                        # This implies if the shortest path is NOT improved, we output 0.
                        # So we only update if new_steps < min_steps.
                        # If new_steps == min_steps, we ignore it because we already have a valid path of that length without adding a word (represented by 0).
                        # Wait, what if the only way to get that length is by adding a word?
                        # No, we calculated min_steps from the original graph. So there IS a path of length min_steps in the original graph.
                        # So we only care if we can GET A SHORTER path.
                    # Therefore, strictly less.
                    pass
    
    if improved:
        print(best_word)
        print(min_steps)
    else:
        print(0)
        print(original_dist)

if __name__ == "__main__":
    solve()