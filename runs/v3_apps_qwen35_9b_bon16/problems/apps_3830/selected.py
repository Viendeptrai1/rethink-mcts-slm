import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    t = int(next(iterator))
    
    results = []
    
    for _ in range(t):
        n = int(next(iterator))
        s = next(iterator)
        
        # We need to count rooms where a cycle exists that includes the room.
        # A room is returnable if it is part of a Strongly Connected Component (SCC) 
        # with size >= 2, OR if it is an SCC of size 1 but has a self-loop.
        # However, since edges only go between distinct nodes (i and i+1), 
        # a self-loop is impossible in the graph structure unless we consider 
        # going out and coming back. But "coming back to it later" implies 
        # a path of length >= 1. 
        #
        # Actually, the condition "leave its room and come back" means there must 
        # be a path from i to i with length >= 1. In a directed graph, this is 
        # equivalent to saying node i is part of a non-trivial SCC (size > 1) 
        # OR if there is a self-loop (which there isn't here directly, but a cycle 
        # of length >= 2 passing through i works).
        #
        # So, we just need to find all nodes that are part of any cycle.
        # Since the graph is a collection of paths and cycles on a circle, 
        # we can determine this by checking reachability.
        #
        # Alternative approach for this specific circular graph structure:
        # 1. If the entire circle is traversable in one direction (all '>' or all '-' allowing wrap), then all are returnable.
        # 2. More generally, a node is part of a cycle if:
        #    - It is in a closed loop formed by '>' and '<' and '-' belts.
        #
        # Let's use a simple reachability check or component analysis.
        # Since N is up to 300,000, O(N) or O(N log N) is needed.
        # 
        # We can model this as finding nodes in non-trivial SCCs.
        # Kosaraju's or Tarjan's algorithm is O(N).
        # Given the constraints and Python speed, Tarjan's is efficient.
        
        # Adjacency list construction
        # Nodes 0 to n-1
        # Edge i -> (i+1)%n if s[i] == '>' or s[i] == '-'
        # Edge (i+1)%n -> i if s[i] == '<' or s[i] == '-'
        
        adj = [[] for _ in range(n)]
        for i in range(n):
            next_node = (i + 1) % n
            if s[i] == '>':
                adj[i].append(next_node)
            elif s[i] == '<':
                adj[next_node].append(i)
            else: # '-'
                adj[i].append(next_node)
                adj[next_node].append(i)
        
        # Tarjan's algorithm
        visited = [False] * n
        stack = []
        on_stack = [False] * n
        ids = [-1] * n
        low = [0] * n
        id_counter = [0]
        scc_count = [0]
        
        def dfs(at):
            visited[at] = True
            ids[at] = low[at] = id_counter[0]
            id_counter[0] += 1
            stack.append(at)
            on_stack[at] = True
            
            for to in adj[at]:
                if not visited[to]:
                    dfs(to)
                    low[at] = min(low[at], low[to])
                elif on_stack[to]:
                    low[at] = min(low[at], ids[to])
            
            if ids[at] == low[at]:
                while stack:
                    node = stack.pop()
                    on_stack[node] = False
                    scc_count[0] += 1
                    if node == at:
                        break
        
        for i in range(n):
            if not visited[i]:
                dfs(i)
        
        # Count returnable rooms
        # A room is returnable if it belongs to an SCC of size > 1.
        # Note: An SCC of size 1 with a self-loop would count, but here edges are between distinct nodes.
        # So any cycle has length >= 2, meaning SCC size >= 2.
        # Wait, what if a node has a self loop? The problem says "leave its room and come back".
        # If there was a self loop, size 1 SCC would count. But our graph construction doesn't have self loops.
        # So strictly, we need SCC size >= 2.
        
        # However, let's re-verify the definition. 
        # "leave its room and come back to it later"
        # Path: u -> v -> ... -> u. Length >= 1.
        # This is exactly the definition of being in a non-trivial SCC (size >= 2) in a graph without self-loops.
        # Since our graph has no self-loops (edges are always between i and i+1), 
        # any cycle involves at least 2 nodes.
        
        returnable = 0
        # We need to know the size of each SCC.
        # We can run Tarjan again or modify to track sizes.
        # Let's just re-run logic to count sizes properly.
        
        visited = [False] * n
        stack = []
        on_stack = [False] * n
        ids = [-1] * n
        low = [0] * n
        id_counter = [0]
        
        scc_sizes = []
        
        def dfs_sizes(at):
            visited[at] = True
            ids[at] = low[at] = id_counter[0]
            id_counter[0] += 1
            stack.append(at)
            on_stack[at] = True
            
            for to in adj[at]:
                if not visited[to]:
                    dfs_sizes(to)
                    low[at] = min(low[at], low[to])
                elif on_stack[to]:
                    low[at] = min(low[at], ids[to])
            
            if ids[at] == low[at]:
                size = 0
                while stack:
                    node = stack.pop()
                    on_stack[node] = False
                    size += 1
                    if node == at:
                        break
                scc_sizes.append(size)
        
        for i in range(n):
            if not visited[i]:
                dfs_sizes(i)
        
        count = 0
        for size in scc_sizes:
            if size >= 2:
                count += size
            # If size == 1, it's a single node with no cycle (since no self loops), so not returnable.
        
        results.append(str(count))

    print('\n'.join(results))

if __name__ == "__main__":
    solve()