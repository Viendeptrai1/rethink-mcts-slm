import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    n = int(input_data[0])
    k = int(input_data[1])

    MOD = 1000000007

    # The structure of the graph must satisfy:
    # 1. From any node in [1, k], we can reach node 1.
    # 2. From any node in [k+1, n], we cannot reach node 1.
    # 3. Starting from 1, we can return to 1 (cycle containing 1).
    # Since each node has exactly one outgoing edge, the graph is a collection of components.
    # Each component contains exactly one cycle.
    # Condition 3 implies that the cycle containing node 1 must exist and be reachable from 1 (which is trivial as 1 is in the cycle).
    # Condition 1 implies that all nodes in [1, k] must be in the same component as node 1, and specifically, the path from any of them must lead to the cycle containing 1.
    # Condition 2 implies that no node in [k+1, n] can reach node 1. This means nodes in [k+1, n] cannot be in the component of node 1.
    # Therefore, the component containing node 1 consists exactly of the set of nodes {1, 2, ..., k}.
    # All nodes in {k+1, ..., n} must form their own components (or be part of other components not containing 1), and crucially, they must not have a path to 1.
    # Since the component {1, ..., k} is closed (in terms of reachability to 1, actually it's a weak component where all edges point towards the cycle), let's refine.
    # Actually, if a node u in [1, k] points to v, if v is in [1, k], fine. If v is in [k+1, n], then starting from u we go to v. From v, can we reach 1?
    # Condition 2 says starting from v (in [k+1, n]) we CANNOT reach 1.
    # But Condition 1 says starting from u (in [1, k]) we MUST reach 1.
    # If u -> v and v cannot reach 1, then u cannot reach 1. Contradiction.
    # Therefore, no node in [1, k] can point to any node in [k+1, n].
    # So, the subgraph induced by [1, k] must contain all edges from nodes in [1, k].
    # Additionally, within the set [1, k], every node must be able to reach 1.
    # This means the component containing 1 is exactly the set [1, k], and it forms a functional graph structure where 1 is part of a cycle, and all other nodes in [1, k] eventually flow into this cycle.
    # Specifically, the set [1, k] forms a connected component in the underlying undirected sense? No, just that all paths from [1, k] stay in [1, k] and lead to 1.
    # Actually, "can reach 1" implies that in the functional graph restricted to [1, k], 1 is in a cycle, and every node in [1, k] has a path to that cycle.
    # Wait, if the component is exactly [1, k], then all edges from [1, k] go to [1, k].
    # And all nodes in [1, k] can reach 1.
    # What about nodes in [k+1, n]? They can point anywhere, but if they point to [1, k], then they can reach 1 (since [1, k] nodes can reach 1).
    # But Condition 2 says nodes in [k+1, n] CANNOT reach 1.
    # So, no node in [k+1, n] can point to any node in [1, k].
    # Thus, the sets [1, k] and [k+1, n] are completely disconnected in terms of edge direction between them.
    # Edges from [1, k] must go to [1, k].
    # Edges from [k+1, n] must go to [k+1, n].

    # So the problem decomposes into two independent counting problems:
    # Part A: Count the number of functional graphs on n=k nodes (labeled 1 to k) such that every node can reach node 1.
    # Part B: Count the number of functional graphs on n-(k) nodes (labeled k+1 to n) with no restrictions other than being a valid functional graph (each node has out-degree 1).
    # The total number of ways is Part A * Part B % MOD.

    # Part B: Number of functions from a set of size m to itself.
    # Each of the m nodes can choose any of the m targets.
    # Count = m^m.
    m = n - k
    if m == 0:
        count_b = 1
    else:
        count_b = pow(m, m, MOD)

    # Part A: Number of functional graphs on k nodes such that all nodes can reach node 1.
    # This is equivalent to counting the number of rooted trees with an extra edge to form a cycle containing the root, where the root is 1?
    # Let's rephrase: In a functional graph component, there is exactly one cycle.
    # If all nodes can reach 1, then 1 must be on the cycle, and the component is a "unicyclic" component where 1 is part of the cycle.
    # Furthermore, there are no other cycles in the component because if there were another cycle, nodes in that cycle could not reach 1 (since they are stuck in the cycle).
    # So the component is a single cycle containing 1, with some trees rooted on the cycle nodes, directing towards the cycle.
    # However, a simpler known result exists: The number of functional graphs on k labeled nodes where a specific node (say 1) is reachable from all other nodes.
    # This is equal to the number of mappings f: {1..k} -> {1..k} such that the iteration f^t(x) = 1 for some t >= 0 for all x.
    # This structure is known as a "rooted functional graph" or simply a component where 1 is the unique attractor.
    # The number of such mappings is given by the sequence related to "number of endofunctions with a unique cycle containing a specific element".
    # Actually, it's simpler: The condition "all nodes can reach 1" means that 1 is in the cycle, and the component is connected (in the weak sense) and contains only the cycle and trees feeding into it.
    # Is it possible for the cycle to be just {1}? Yes.
    # Is it possible for the cycle to be {1, 2}? Yes, if 1->2 and 2->1, and others feed in.
    # The number of such functions on k nodes where a specific node 1 is reachable from all nodes is known to be:
    # Sum_{j=1 to k} (C(k-1, j-1) * (j-1)! * j^{k-j}) ? Let's derive or recall.
    # Alternative approach:
    # Consider the set of nodes that are on the cycle. Let the cycle length be j.
    # The cycle must contain 1. So we choose j-1 other nodes from the remaining k-1 nodes to be on the cycle.
    # Number of ways to choose the other j-1 nodes: C(k-1, j-1).
    # Number of ways to arrange these j nodes in a cycle containing 1: (j-1)! (since 1 is fixed, we arrange the rest in a circle).
    # The remaining k-j nodes form trees rooted on the j cycle nodes. Each of these k-j nodes must eventually reach the cycle.
    # This is equivalent to forming a functional graph on k nodes where the image of the k-j nodes eventually hits the cycle.
    # Actually, the standard formula for the number of functional graphs on k nodes where a specific node 1 is in the cycle and all nodes reach 1 is:
    # k^{k-1} ? No, that's for spanning trees (Cayley).
    # Let's use the property: The number of mappings f: [k] -> [k] such that 1 is reachable from all x is equal to the number of "rooted mappings" at 1.
    # There is a known identity: The number of such functions is k^{k-1} * something?
    # Let's try small k.
    # k=1: Only 1->1. Count = 1. Formula k^{k-1} = 1^0 = 1. Correct.
    # k=2: Nodes {1, 2}.
    # Possible functions:
    # 1->1, 2->1 (2 reaches 1, 1 reaches 1). OK.
    # 1->2, 2->1 (cycle 1-2). OK.
    # 1->2, 2->2 (2 reaches 2, 1 reaches 2->2. 1 cannot reach 1? Wait. Condition: "he can get back to house number 1". This implies 1 is in a cycle. If 1->2 and 2->2, 1 goes to 2 and stays there. Never returns to 1. So this is invalid.)
    # So for k=2, valid:
    # 1->1, 2->1
    # 1->2, 2->1
    # Total 2.
    # My previous manual enumeration missed the cycle condition for 1.
    # Let's re-evaluate k=2.
    # Valid if: 1 is in a cycle, and all nodes reach 1.
    # Cases:
    # Cycle {1}: 1->1. Then 2 must reach 1. 2->1. (1 way)
    # Cycle {1, 2}: 1->2, 2->1. (1 way)
    # Total 2.
    # Formula k^{k-1} = 2^1 = 2. Matches.
    # k=3: Nodes {1, 2, 3}.
    # Formula guess: 3^{3-1} = 9.
    # Let's list or verify logic.
    # It is a known result that the number of functional graphs on n nodes such that a specific node is part of the unique cycle and all nodes reach it is n^{n-1}.
    # Wait, let me double check with k=3.
    # If the formula is k^{k-1}, then for k=3, answer is 9.
    # Let's try to construct.
    # Cycle length 1: {1}. 1->1. Remaining {2, 3} must reach 1.
    # Maps from {2, 3} to {1, 2, 3} such that they eventually hit 1.
    # Since 1 is fixed, effectively we need 2 and 3 to map into the component of 1.
    # This is equivalent to forming a tree rooted at 1 on nodes {1, 2, 3} with edges directed towards root?
    # No, in functional graphs, edges are x -> f(x). So it's edges directed towards the cycle.
    # If cycle is {1}, then 1->1. 2 and 3 must eventually reach 1.
    # This forms a tree rooted at 1 with edges directed towards 1.
    # Number of such trees on 3 labeled nodes rooted at 1 is 2^{3-2} * 1? No.
    # Cayley's formula: Number of spanning trees on k nodes is k^{k-2}. Here rooted at 1, so (k-1)^{k-2}? No.
    # The number of functional components on k nodes where the cycle is a single node (1) is the number of trees rooted at 1.
    # A tree rooted at 1 with edges directed towards 1 corresponds to a mapping where f(1)=1 and the rest form a tree structure flowing to 1.
    # The number of such mappings where the image of x is its parent, and root is 1, is (k-1)^{k-2}? No.
    # Let's use the sequence A000272 or similar.
    # Actually, the number of mappings f: [k] -> [k] such that 1 is in the cycle and all reach 1 is exactly k^{k-1}.
    # Let's verify k=3 manually.
    # Cycle {1}: 1->1. We need 2 and 3 to reach 1.
    # Possible mappings for 2, 3:
    # 2->1, 3->1
    # 2->1, 3->2 (3->2->1)
    # 2->3, 3->1 (2->3->1)
    # 2->3, 3->2 (3->2->3, stuck in 2-3, never reach 1). Invalid.
    # So for cycle {1}, we have 3 valid mappings.
    # Cycle {1, 2}: 1->2, 2->1. 3 must reach {1, 2}.
    # 3 can map to 1 or 2. (2 choices).
    # So 2 valid mappings.
    # Cycle {1, 3}: 1->3, 3->1. 2 must reach {1, 3}.
    # 2 can map to 1 or 3. (2 choices).
    # So 2 valid mappings.
    # Total = 3 + 2 + 2 = 7.
    # But 3^{3-1} = 9. My count is 7.
    # Where are the missing 2?
    # Did I miss cycles?
    # Cycle {1, 2, 3}: 1->2->3->1 (1 permutation). 1->3->2->1 (1 permutation). Total 2.
    # Ah, I missed the case where the cycle length is 3.
    # So total = 3 (len 1) + 2 (len 2 via 2) + 2 (len 2 via 3) + 2 (len 3) = 9.
    # Matches 3^2 = 9.
    # So the formula for Part A is indeed k^{k-1}.

    count_a = pow(k, k - 1, MOD)

    ans = (count_a * count_b) % MOD
    print(ans)

if __name__ == '__main__':
    solve()