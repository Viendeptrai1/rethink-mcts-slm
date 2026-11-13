def count_joke_sets(N, jokes, hierarchy):
    from collections import defaultdict

    # Build adjacency list for the hierarchy
    adj = defaultdict(list)
    for A, B in hierarchy:
        adj[A].append(B)

    def dfs(node, parent, joke_set):
        if node == 1:  # Petar's node
            if len(joke_set) > 1:
                return 0
            return 1
        
        valid = 0
        for neighbor in adj[node]:
            if neighbor != parent:
                neighbor_jokes = set()
                if dfs(neighbor, node, neighbor_jokes):
                    if neighbor_jokes.issubset(range(min(joke_set), max(joke_set) + 2)):
                        new_joke_set = joke_set.union(neighbor_jokes)
                        if len(new_joke_set) == len(set(new_joke_set)) and len(new_joke_set) >= 2:
                            valid += 1
        return valid

    return dfs(1, -1, {jokes[0]})

# Example usage
import sys
input = sys.stdin.read
data = input().split()

N = int(data[0])
jokes = [int(x) for x in data[1:N+1]]
hierarchy = [(int(a), int(b)) for a, b in zip(data[N+1::2], data[N+2::2])]

print(count_joke_sets(N, jokes, hierarchy))