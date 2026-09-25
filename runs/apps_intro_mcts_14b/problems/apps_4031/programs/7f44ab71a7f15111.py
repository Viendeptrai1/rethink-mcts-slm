import sys
from collections import defaultdict, deque

def is_substring(s1, s2):
    return s1 in s2

def topological_sort(graph, indegree):
    queue = deque([node for node in indegree if indegree[node] == 0])
    result = []

    while queue:
        node = queue.popleft()
        result.append(node)
        for neighbor in graph[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    return result

def can_reorder_strings(strings):
    n = len(strings)
    graph = defaultdict(list)
    indegree = {s: 0 for s in strings}

    for i in range(n):
        for j in range(i + 1, n):
            if is_substring(strings[i], strings[j]):
                graph[strings[i]].append(strings[j])
                indegree[strings[j]] += 1
            elif is_substring(strings[j], strings[i]):
                graph[strings[j]].append(strings[i])
                indegree[strings[i]] += 1

    sorted_order = topological_sort(graph, indegree)

    if len(sorted_order) != n:
        return "NO"
    else:
        return "YES\n" + "\n".join(sorted_order)

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    strings = data[1:n+1]
    
    result = can_reorder_strings(strings)
    print(result)