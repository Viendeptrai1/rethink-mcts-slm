import sys
from collections import defaultdict, deque

def count_valid_joke_sets(N, V, edges):
    # Build the tree
    tree = defaultdict(list)
    for A, B in edges:
        tree[A].append(B)
    
    # Function to check if a list of numbers is consecutive
    def is_consecutive(lst):
        lst.sort()
        return all(lst[i] + 1 == lst[i + 1] for i in range(len(lst) - 1))
    
    # DFS to explore all valid subsets
    def dfs(node, parent, current_set):
        if len(current_set) > 0 and not is_consecutive(current_set):
            return 0
        
        # Count the current valid subset
        count = 1 if len(current_set) > 0 else 0
        
        # Explore children
        for child in tree[node]:
            if child != parent:
                new_set = current_set.copy()
                if V[child - 1] not in new_set:
                    new_set.add(V[child - 1])
                count += dfs(child, node, new_set)
        
        return count
    
    # Start DFS from Petar (node 1)
    return dfs(1, None, set())

# Read input
input = sys.stdin.read
data = input().split()
N = int(data[0])
V = list(map(int, data[1:N+1]))
edges = [(int(data[N+1 + 2*i]), int(data[N+2 + 2*i])) for i in range(N-1)]

# Output the result
print(count_valid_joke_sets(N, V, edges))