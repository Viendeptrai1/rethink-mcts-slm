import sys
from collections import defaultdict, deque

def process_queries(n, q, superiors, queries):
    # Build the tree structure
    tree = defaultdict(list)
    for i in range(2, n + 1):
        tree[superiors[i - 2]].append(i)
    
    # Function to perform DFS and get the order of command spreading
    def dfs_spread(start):
        order = []
        stack = [start]
        visited = set()
        
        while stack:
            current = stack.pop()
            if current not in visited:
                visited.add(current)
                order.append(current)
                # Add children in reverse order to process the smallest index first
                for child in sorted(tree[current], reverse=True):
                    stack.append(child)
        
        return order
    
    results = []
    for u, k in queries:
        order = dfs_spread(u)
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
    superiors = list(map(int, data[2:n]))
    queries = []
    
    index = n
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