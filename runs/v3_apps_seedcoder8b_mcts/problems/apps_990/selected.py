import sys
from collections import defaultdict

sys.setrecursionlimit(10**6)

def count_valid_colorings(N, edges, M, restrictions):
    # Build the adjacency list for the tree
    tree = defaultdict(list)
    for a, b in edges:
        tree[a].append(b)
        tree[b].append(a)

    # Prepare the restrictions as a set of frozensets for quick lookup
    restrictions_set = set(frozenset((u, v)) for u, v in restrictions)

    # Memoization dictionary
    memo = {}

    def dfs(node, parent, black_edges):
        # Check if the current state has been computed before
        state = (node, parent, black_edges)
        if state in memo:
            return memo[state]

        # Initialize the count of valid colorings for this subtree
        count = 1  # Start with the assumption that this subtree can be painted in one valid way

        # Traverse all children
        for neighbor in tree[node]:
            if neighbor == parent:
                continue

            # Check if the edge (node, neighbor) is in any of the restrictions
            if frozenset((node, neighbor)) in restrictions_set:
                # If it is, we must paint it black in at least one valid coloring
                count *= dfs(neighbor, node, True)
            else:
                # If it's not, we can choose to paint it black or white
                count *= (dfs(neighbor, node, True) + dfs(neighbor, node, False))

        # If there are black edges in the path, we must paint this subtree in a valid way
        if black_edges:
            memo[state] = count
        else:
            # If there are no black edges in the path, we can choose to paint this subtree in a valid way or not
            memo[state] = count * 2

        return memo[state]

    # Start DFS from node 1 (or any node, as the tree is connected)
    total_count = dfs(1, -1, False)

    # Since we counted each valid coloring twice (once for each root), divide by 2
    return total_count // 2

def main():
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    N = int(data[index])
    index += 1
    
    edges = []
    for _ in range(N - 1):
        a = int(data[index])
        b = int(data[index + 1])
        edges.append((a, b))
        index += 2
    
    M = int(data[index])
    index += 1
    
    restrictions = []
    for _ in range(M):
        u = int(data[index])
        v = int(data[index + 1])
        restrictions.append((u, v))
        index += 2
    
    result = count_valid_colorings(N, edges, M, restrictions)
    print(result)

if __name__ == "__main__":
    main()