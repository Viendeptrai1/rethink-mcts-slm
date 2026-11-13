from collections import defaultdict, deque

def count_valid_joke_sets(N, joke_types, superior_pairs):
    # Build the tree structure
    tree = defaultdict(list)
    for A, B in superior_pairs:
        tree[A].append(B)
    
    # Function to check if a set of jokes is valid
    def is_valid_set(jokes):
        return len(set(jokes)) == len(jokes) and all(abs(a - b) == 1 for a, b in zip(sorted(jokes), sorted(jokes)[1:]))
    
    # DFS to find all valid subsets of jokes
    def dfs(node, parent_jokes):
        current_jokes = parent_jokes + [joke_types[node - 1]]
        if is_valid_set(current_jokes):
            valid_sets.add(tuple(sorted(current_jokes)))
        
        for child in tree[node]:
            dfs(child, current_jokes)
    
    valid_sets = set()
    dfs(1, [])
    
    return len(valid_sets)

# Read input
import sys
input = sys.stdin.read
data = input().split()

N = int(data[0])
joke_types = list(map(int, data[1:N+1]))
superior_pairs = [(int(data[N+i*2]) - 1, int(data[N+i*2+1]) - 1) for i in range(N-1)]

# Output the result
print(count_valid_joke_sets(N, joke_types, superior_pairs))