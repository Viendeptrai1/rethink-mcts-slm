import sys

# Increase recursion depth just in case, though we use iterative approaches
sys.setrecursionlimit(20000)

def solve():
    # Read all input from stdin at once
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        t_str = next(iterator)
        t = int(t_str)
    except StopIteration:
        return

    for _ in range(t):
        try:
            n = int(next(iterator))
            a = []
            for _ in range(n):
                a.append(int(next(iterator)))
        except StopIteration:
            break

        # Check if all districts belong to the same gang
        # If so, we cannot connect any two directly without causing a revolt
        # because any edge would connect two nodes of the same gang.
        # Thus, if there's only 1 distinct gang ID, it's impossible.
        unique_gangs = set(a)
        
        if len(unique_gangs) == 1:
            print("NO")
            continue
        
        # If there are at least 2 distinct gangs, a solution always exists.
        # Strategy:
        # 1. Identify one gang that appears at least twice (majority or just not unique).
        #    Actually, a simpler strategy:
        #    Find two indices i and j such that a[i] != a[j].
        #    Then, connect all other nodes to either i or j, ensuring the neighbor has a different gang.
        #
        # Better constructive approach:
        # Since there are at least 2 gangs, pick two nodes u and v with different gangs.
        # We can form a "backbone" connecting all nodes of gang A to a specific node of gang B,
        # and all nodes of gang B to a specific node of gang A? No, that might not work directly.
        #
        # Let's try a specific construction:
        # 1. Find an index `first` such that a[first] is some gang X.
        # 2. Find an index `second` such that a[second] is some gang Y (Y != X).
        # 3. We want to build a tree.
        # 4. Connect `second` to every node `i` where a[i] != Y.
        #    Since a[second] = Y, and a[i] != Y, this edge is valid.
        #    This connects all non-Y nodes to `second`.
        #    But what about nodes with gang Y? They are connected to `second`? No, a[i] == Y means invalid edge to `second`.
        #
        # Revised Strategy:
        # Since there are at least 2 gangs, let's find two nodes with different gangs: u and v.
        # Let u be an index with gang G1, v be an index with gang G2.
        #
        # We can connect u to all nodes that do NOT have gang G1.
        #   For any node w with a[w] != G1, edge (u, w) is valid because a[u]=G1 != a[w].
        #   This connects all non-G1 nodes to u.
        #
        # We can connect v to all nodes that do NOT have gang G2.
        #   For any node w with a[w] != G2, edge (v, w) is valid.
        #   This connects all non-G2 nodes to v.
        #
        # Now, consider the graph:
        # - All nodes with gang != G1 are connected to u.
        # - All nodes with gang != G2 are connected to v.
        # - u and v are connected? Only if a[u] != a[v], which is true by selection.
        #   So add edge (u, v).
        #
        # Does this cover all nodes?
        # - Nodes with gang == G1:
        #   They are NOT connected to v (since a[node]=G1, and if G1==G2, impossible, but G1!=G2).
        #   Wait, if a[node] == G1, then a[node] != G2 is TRUE. So they are connected to v.
        #   Correct: If a[node] == G1, then a[node] != G2 (since G1 != G2), so edge (v, node) is valid.
        # - Nodes with gang == G2:
        #   They are NOT connected to u (since a[node]=G2 != G1 is true, so edge (u, node) is valid).
        #   Wait, if a[node] == G2, then a[node] != G1 is TRUE. So edge (u, node) is valid.
        #
        # So:
        # 1. Pick u with gang G1, v with gang G2 (G1 != G2).
        # 2. Connect u to all nodes w where a[w] != G1.
        # 3. Connect v to all nodes w where a[w] != G2.
        # 4. Connect u and v.
        #
        # Let's verify connectivity:
        # - All nodes with G1 are connected to v.
        # - All nodes with G2 are connected to u.
        # - All other nodes (G3, etc.) are connected to both u and v (since G3 != G1 and G3 != G2).
        # - u and v are connected.
        # Therefore, the whole graph is connected.
        #
        # Are edges valid?
        # - (u, v): G1 != G2. Valid.
        # - (u, w) where a[w] != G1: G1 != a[w]. Valid.
        # - (v, w) where a[w] != G2: G2 != a[w]. Valid.
        #
        # Number of edges:
        # - 1 edge (u, v)
        # - Count(w where a[w] != G1)
        # - Count(w where a[w] != G2)
        # Total nodes = n.
        # Sum of degrees in this logic?
        # Actually, we just need n-1 edges.
        # The set of edges defined:
        # E = {(u, v)} U {(u, w) | a[w] != G1} U {(v, w) | a[w] != G2}
        # Is it possible to have duplicate edges or cycles?
        # We need exactly n-1 edges forming a tree.
        # Let's count:
        # Nodes with G1: count1. They connect to v. (count1 edges)
        # Nodes with G2: count2. They connect to u. (count2 edges)
        # Other nodes: count_other = n - count1 - count2.
        #   For these nodes, a[w] != G1 and a[w] != G2.
        #   So they connect to u AND to v. That creates 2 edges per node?
        #   Yes, (u, w) and (v, w).
        # Total edges = 1 + count1 + count2 + 2*count_other.
        # This is definitely > n-1 if count_other > 0.
        #
        # We need a simpler construction that yields exactly n-1 edges.
        #
        # Alternative Construction:
        # 1. Find u (gang G1) and v (gang G2).
        # 2. Connect u to ALL nodes w such that a[w] != G1.
        #    This covers all nodes except those with gang G1 (including u itself, but we skip self).
        #    Let S1 = {w | a[w] != G1, w != u}.
        #    Edges: (u, w) for w in S1.
        #    These edges connect u to everyone not in G1.
        #    The component containing u now includes u and all non-G1 nodes.
        #    The nodes remaining unconnected to this component are exactly those with gang G1 (excluding u).
        # 3. Now, we need to connect the remaining G1 nodes to the main component.
        #    We know v is a node with gang G2, so v is in the main component (since G2 != G1).
        #    We can connect every remaining G1 node (w where a[w] == G1, w != u) to v.
        #    Edge (v, w): a[v]=G2, a[w]=G1. Since G1 != G2, this is valid.
        #
        # Let's count edges:
        # - Edges from step 2: (u, w) for all w != u with a[w] != G1.
        #   Count = n - count(G1).
        # - Edges from step 3: (v, w) for all w != u, w with a[w] == G1.
        #   Count = count(G1) - 1 (since u is excluded).
        # Total edges = (n - count(G1)) + (count(G1) - 1) = n - 1.
        # Perfect.
        #
        # Connectivity:
        # - All non-G1 nodes are connected to u.
        # - All G1 nodes (except u) are connected to v.
        # - u and v are connected?
        #   u has gang G1. v has gang G2.
        #   Is v connected to u?
        #   v is a non-G1 node (since G2 != G1). So in step 2, v is connected to u via (u, v).
        #   Yes.
        # So the graph is connected.
        
        # Implementation:
        # 1. Find u and v.
        # 2. Generate edges.
        
        # Find u
        u = -1
        for i in range(n):
            u = i
            break
        
        # Find v with different gang
        v = -1
        for i in range(n):
            if i == u:
                continue
            if a[i] != a[u]:
                v = i
                break
        
        if v == -1:
            # Should be caught by unique_gangs check, but safety
            print("NO")
            continue
            
        g1 = a[u]
        
        edges = []
        
        # Step 2: Connect u to all w where a[w] != g1
        for i in range(n):
            if i == u:
                continue
            if a[i] != g1:
                edges.append((u + 1, i + 1))
        
        # Step 3: Connect v to all w where a[w] == g1 (and w != u)
        for i in range(n):
            if i == u:
                continue
            if a[i] == g1:
                edges.append((v + 1, i + 1))
        
        # We have exactly n-1 edges.
        print("YES")
        for x, y in edges:
            print(f"{x} {y}")

if __name__ == "__main__":
    solve()