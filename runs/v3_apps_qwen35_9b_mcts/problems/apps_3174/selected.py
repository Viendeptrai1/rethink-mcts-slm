import sys

# Increase recursion depth just in case, though we will use iterative approaches where possible.
sys.setrecursionlimit(200000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        K = int(next(iterator))
    except StopIteration:
        return

    cities = []
    for _ in range(N):
        x = int(next(iterator))
        y = int(next(iterator))
        k = int(next(iterator))
        cities.append((x, y, k))

    # If K is 1, any non-empty subset sum is divisible by 1. 
    # Since there is at least one city, D=0 works.
    if K == 1:
        print("0.000")
        return

    # Precompute all pairwise distances
    # We need to store (distance, u, v)
    edges = []
    for i in range(N):
        for j in range(i + 1, N):
            x1, y1, _ = cities[i]
            x2, y2, _ = cities[j]
            dist_sq = (x1 - x2)**2 + (y1 - y2)**2
            dist = dist_sq ** 0.5
            edges.append((dist, i, j))

    # Sort edges by distance
    edges.sort(key=lambda x: x[0])

    # Union-Find data structure
    parent = list(range(N))
    rank = [0] * N

    def find(i):
        path = []
        while i != parent[i]:
            path.append(i)
            i = parent[i]
        for node in path:
            parent[node] = i
        return i

    def union(i, j):
        root_i = find(i)
        root_j = find(j)
        if root_i == root_j:
            return root_i
        if rank[root_i] < rank[root_j]:
            root_i, root_j = root_j, root_i
        parent[root_j] = root_i
        if rank[root_i] == rank[root_j]:
            rank[root_i] += 1
        return root_i

    # DP state: dp[root] = set of reachable subset sums modulo K for the component rooted at 'root'
    # We use a dictionary to map root -> set of residues.
    # To optimize, we only store sets for active roots.
    dp = {}

    # Initialize: each city is its own component with its own residue
    for i in range(N):
        r = cities[i][2] % K
        dp[i] = {r}

    # Iterate through sorted edges
    for dist, u, v in edges:
        root_u = find(u)
        root_v = find(v)

        if root_u == root_v:
            continue

        # Retrieve the sets BEFORE merging to avoid KeyError if logic changes root
        set_u = dp[root_u]
        set_v = dp[root_v]

        # Check if either set already contains 0 (though with the problem statement "no city divisible by K",
        # a single city never has 0. So we only get 0 after merging).
        # However, we must check the new component formed by merging.
        
        # Merge logic:
        # New set = { (a + b) % K | a in set_u, b in set_v } U set_u U set_v
        # Actually, the subset sum of the union of two sets is the Minkowski sum of their subset sums.
        # The new component's reachable sums are the union of:
        # 1. Sums from set_u (subsets entirely in u)
        # 2. Sums from set_v (subsets entirely in v)
        # 3. Sums from (subset in u) + (subset in v)
        
        # Optimization: If either set is already {0}, we are done. But initially no set has 0.
        # We need to check if 0 is in the new combined set.
        
        # Calculate new sums
        new_sums = set()
        
        # Add existing sums
        new_sums.update(set_u)
        new_sums.update(set_v)
        
        # Add combined sums
        # To optimize, if either set is large, this O(|A|*|B|) might be slow.
        # However, K is small (<=30). The size of any set is at most K.
        # So |set_u| <= K, |set_v| <= K. The product is at most 900.
        # This is very fast.
        
        for a in set_u:
            for b in set_v:
                new_sums.add((a + b) % K)
        
        # Check if 0 is reachable
        if 0 in new_sums:
            print(f"{dist:.3f}")
            return

        # Perform Union
        # We need to decide which root becomes the parent.
        # Let's make root_u the parent of root_v.
        # We must update dp[root_u] to be new_sums.
        # We must delete dp[root_v] because it's no longer a root.
        
        # Ensure we don't access dp[root_v] after deletion in a way that causes issues.
        # We already captured set_v.
        
        # Update parent
        parent[root_v] = root_u
        if rank[root_u] == rank[root_v]:
            rank[root_u] += 1
        
        # Update DP
        dp[root_u] = new_sums
        # Remove the old entry for root_v
        if root_v in dp:
            del dp[root_v]

    # The problem guarantees a solution exists.
    # If we finish the loop without returning, something is wrong, but theoretically impossible given constraints.
    # However, if N=1, the loop doesn't run, but the problem says "subset of cities", and "no city divisible by K".
    # If N=1, no subset sum is divisible by K. But the problem says "input data will be such that there is always a solution".
    # This implies N >= K or some combination allows it.
    # Wait, if N < K, it's possible no solution exists unless we consider the whole set.
    # But the problem guarantees a solution.
    # If the loop finishes, it means we connected everything and still didn't find 0?
    # That shouldn't happen if a solution exists.
    # Just in case, if we exit loop, it means D is effectively infinity or we missed something.
    # But with "always a solution", we should have returned inside the loop.
    # The only case is if N=1 and K=1, handled at start.
    # If N > 1 and solution exists, we will find it.

if __name__ == '__main__':
    solve()