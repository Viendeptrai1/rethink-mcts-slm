import sys

def find_optimal_reconstruction(fragments):
    n = len(fragments)
    graph = [[] for _ in range(n)]
    lengths = [0] * n
    
    # Build the graph and calculate lengths
    for i in range(n):
        for j in range(n):
            if i != j:
                suffix_i = fragments[i][-5:]
                prefix_j = fragments[j][:5]
                if suffix_i == prefix_j:
                    graph[i].append(j)
                    lengths[i] += len(suffix_i)
    
    # Find all Eulerian paths
    def dfs(node, path):
        while graph[node]:
            neighbor = graph[node].pop()
            dfs(neighbor, path)
            path.append(fragments[neighbor])
        result.append(path[::-1])
    
    result = []
    for i in range(n):
        if len(graph[i]) % 2 == 1:
            return "AMBIGUOUS"
        dfs(i, [fragments[i]])
    
    # Check for uniqueness
    if len(result) > 1:
        return "AMBIGUOUS"
    
    # Reconstruct the text
    reconstructed_text = result[0][0]
    for fragment in result[0][1:]:
        suffix_length = min(len(reconstructed_text), 5)
        reconstructed_text += fragment[suffix_length:]
    
    return reconstructed_text

# Read input
input = sys.stdin.read
data = input().splitlines()

# Parse input
n = int(data[0])
fragments = data[1:]

# Find and print the optimal reconstruction
print(find_optimal_reconstruction(fragments))