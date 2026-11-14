import sys

# Increase recursion depth just in case, though we use iterative approach
sys.setrecursionlimit(300000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        n = int(next(iterator))
        m = int(next(iterator))
    except StopIteration:
        return

    edges = []
    degree = [0] * (n + 1)
    
    # Read edges
    for i in range(m):
        u = int(next(iterator))
        v = int(next(iterator))
        edges.append((u, v))
        degree[u] += 1
        degree[v] += 1

    # Condition 1: The graph must be a tree (no cycles) to avoid paths of length >= 2 in any orientation?
    # Actually, if there is a cycle, can we orient it to have no path of length >= 2?
    # If we have a cycle, every vertex in the cycle has degree at least 2 within the cycle.
    # If we orient edges, say u->v and v->w, then u->v->w is a path of length 2.
    # To avoid paths of length >= 2, every vertex can have at most one incoming edge and at most one outgoing edge?
    # No, the condition is "no paths of length two or greater".
    # This means there is no sequence v1 -> v2 -> v3.
    # This implies that for any vertex v, it cannot have both an incoming edge and an outgoing edge.
    # So every vertex must be either a source (only outgoing) or a sink (only incoming) or isolated.
    # If a vertex has an incoming edge, it cannot have an outgoing edge.
    # If a vertex has an outgoing edge, it cannot have an incoming edge.
    # This means the directed graph is a collection of stars where edges point either all towards the center or all away from the center.
    # But the graph is connected.
    # If the graph is connected and we have such an orientation:
    # Case 1: All edges point towards a center C. Then C has only incoming edges, leaves have only outgoing.
    #   Path: leaf -> C. Length 1. No leaf -> C -> leaf because C has no outgoing.
    #   This works.
    # Case 2: All edges point away from a center C. Then C has only outgoing, leaves have only incoming.
    #   Path: C -> leaf. Length 1. No leaf -> C -> leaf because leaves have no outgoing.
    #   This works.
    # Case 3: Mixed? If there is a path of length 2, it fails.
    #   If we have u->v and v->w, fail.
    #   So no vertex can have in-degree >= 1 and out-degree >= 1.
    #   In a connected graph with m >= n-1:
    #   If m > n-1, there is a cycle.
    #   In a cycle, can we orient without paths of length 2?
    #   Cycle: 1-2-3-1.
    #   Orient 1->2, 2->3, 3->1. Path 1->2->3 (len 2). Fail.
    #   Orient 1->2, 2<-3, 3->1. Path 3->1->2 (len 2). Fail.
    #   Any orientation of a cycle of length >= 3 will have a path of length 2?
    #   Yes, because in a cycle, you can't have all edges pointing to one node (that would require multiple edges or not be a simple cycle) and you can't have all pointing away.
    #   Actually, if you have a cycle, you must have at least one "turn" or a node with in and out?
    #   Sum of in-degrees = m. Sum of out-degrees = m.
    #   If no node has both in>0 and out>0, then the graph is a set of components where each component is a star (all in or all out).
    #   Since the original graph is connected, the directed graph must be connected (weakly).
    #   If the directed graph is a set of stars, and the underlying undirected graph is connected, then the whole thing must be one star.
    #   Therefore, the underlying graph MUST be a star graph.
    #   A star graph has n vertices and n-1 edges.
    #   So if m != n-1, output NO.
    #   If m == n-1, it's a tree. Is every tree a star? No.
    #   So we must check if the tree is a star graph.
    #   A star graph has exactly one vertex with degree n-1, and all others with degree 1.
    #   If such a vertex exists, we can orient all edges towards it or all away from it.
    #   If no such vertex exists (i.e., max degree < n-1), then it's not a star, so we cannot satisfy the condition. Output NO.

    # Check 1: Must be a tree (m == n-1)
    if m != n - 1:
        print("NO")
        return

    # Check 2: Must be a star graph
    # Find the center
    center = -1
    for i in range(1, n + 1):
        if degree[i] == n - 1:
            center = i
            break
    
    if center == -1:
        print("NO")
        return

    # Now we have a star graph with center 'center'.
    # We need to orient edges.
    # Option A: All edges point TO center.
    #   For edge (u, v):
    #     If u == center, we need u -> v? No, we need v -> u (pointing to center).
    #     Wait, if edge is u, v.
    #     If u is center, we want v -> u. So direction is v to u.
    #     Input format: u, v.
    #     If we want v -> u, that is '1' (since '1' means v -> u, i.e., from second to first).
    #     If v is center, we want u -> v. That is '0'.
    # Option B: All edges point FROM center.
    #   If u is center, we want u -> v. That is '0'.
    #   If v is center, we want v -> u. That is '1'.
    
    # Both options are valid. Let's pick Option A (all towards center) arbitrarily.
    # Or Option B. Let's do Option A: all edges directed towards the center.
    # Edge i: u, v
    # If u == center: we need v -> u. Output '1'.
    # If v == center: we need u -> v. Output '0'.
    # Note: u != v and one of them is center.
    
    result = []
    for u, v in edges:
        if u == center:
            # Need v -> u, so direction is from v to u.
            # Input is u, v. We want v -> u.
            # '0' means u -> v. '1' means v -> u.
            result.append('1')
        else:
            # v must be center
            # Need u -> v.
            # '0' means u -> v.
            result.append('0')
    
    print("YES")
    print("".join(result))

if __name__ == '__main__':
    solve()