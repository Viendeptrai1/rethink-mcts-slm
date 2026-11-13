import sys

def find_optimal_reconstruction(fragments):
    n = len(fragments)
    graph = {i: set() for i in range(n)}
    
    def get_overlap(a, b):
        for i in range(5, min(len(a), len(b)) + 1):
            if a[-i:] == b[:i]:
                return i
        return 0
    
    for i in range(n):
        for j in range(n):
            if i != j:
                overlap = get_overlap(fragments[i], fragments[j])
                if overlap >= 5:
                    graph[i].add(j)
    
    def dfs(node):
        stack = [node]
        visited = [False] * n
        while stack:
            node = stack.pop()
            if not visited[node]:
                visited[node] = True
                for neighbor in graph[node]:
                    stack.append(neighbor)
        
        return sum(not v for v in visited)
    
    max_cliques = []
    max_size = 0
    
    for i in range(n):
        clique = [i]
        for j in range(i + 1, n):
            valid = True
            for k in clique:
                if j not in graph[k]:
                    valid = False
                    break
            if valid:
                clique.append(j)
        if len(clique) > max_size:
            max_size = len(clique)
            max_cliques = [clique]
        elif len(clique) == max_size:
            max_cliques.append(clique)
    
    if len(max_cliques) > 1:
        return "AMBIGUOUS"
    
    for clique in max_cliques:
        for i in range(len(clique)):
            for j in range(i + 1, len(clique)):
                if len(graph[clique[i]]) < len(graph[clique[j]]):
                    clique[i], clique[j] = clique[j], clique[i]
    
    for clique in max_cliques:
        result = []
        for i in clique:
            prefix_length = get_overlap(fragments[clique[clique.index(i)-1]], fragments[i]) if i != clique[0] else 0
            result.append(fragments[i][prefix_length:])
        print(''.join(result))

if __name__ == "__main__":
    n = int(sys.stdin.readline().strip())
    fragments = [sys.stdin.readline().strip() for _ in range(n)]
    find_optimal_reconstruction(fragments)