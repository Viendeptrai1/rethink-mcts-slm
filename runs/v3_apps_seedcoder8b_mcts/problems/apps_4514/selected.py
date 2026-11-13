import sys
from collections import defaultdict, deque

def process_queries(n, q, superiors, queries):
    # Build the tree from the superiors list
    tree = defaultdict(list)
    for i in range(2, n + 1):
        tree[superiors[i - 2]].append(i)
    
    # Function to perform DFS and collect the order of officers receiving the command
    def dfs(node, order):
        order.append(node)
        for child in sorted(tree[node]):
            dfs(child, order)
    
    results = []
    for u, k in queries:
        order = []
        dfs(u, order)
        if k <= len(order):
            results.append(order[k - 1])
        else:
            results.append(-1)
    
    return results

def main():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    q = int(data[1])
    superiors = list(map(int, data[2:n + 1]))
    queries = []
    
    index = n + 1
    for _ in range(q):
        u = int(data[index])
        k = int(data[index + 1])
        queries.append((u, k))
        index += 2
    
    results = process_queries(n, q, superiors, queries)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()