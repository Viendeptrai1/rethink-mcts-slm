from typing import List
import sys

def dfs(tree, start, visited, order):
    visited[start] = True
    for neighbor in tree[start]:
        if not visited[neighbor]:
            dfs(tree, neighbor, visited, order)
            order.append(neighbor)

def get_order(tree, start):
    visited = [False] * len(tree)
    order = []
    dfs(tree, start, visited, order)
    return order[::-1]

def solve(n: int, q: int, parents: List[int], queries: List[List[int]]) -> List[int]:
    tree = [[] for _ in range(n + 1)]
    for i in range(2, n + 1):
        tree[parents[i - 1]].append(i)
    
    orders = [get_order(tree, i) for i in range(1, n + 1)]
    
    results = []
    for ui, ki in queries:
        if ki <= len(orders[ui - 1]):
            results.append(orders[ui - 1][ki - 1])
        else:
            results.append(-1)
    
    return results

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    q = int(data[1])
    
    parents = list(map(int, data[2:n+1]))
    
    queries = []
    for i in range(q):
        ui = int(data[n+1+i*2])
        ki = int(data[n+2+i*2])
        queries.append([ui, ki])
    
    result = solve(n, q, parents, queries)
    
    for res in result:
        print(res)