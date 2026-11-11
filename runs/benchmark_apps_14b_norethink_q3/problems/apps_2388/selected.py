import sys
from typing import List, Tuple

MOD = 998244353

def count_independent_sets(n: int, robots: List[Tuple[int, int]]) -> int:
    # Sort robots by their starting position
    robots.sort()
    
    # Find all connected components
    components = []
    visited = [False] * n
    
    def dfs(start: int):
        stack = [start]
        component = []
        while stack:
            node = stack.pop()
            if not visited[node]:
                visited[node] = True
                component.append(node)
                for neighbor in range(node + 1, n):
                    if not visited[neighbor] and robots[neighbor][0] < robots[node][0] + robots[node][1]:
                        stack.append(neighbor)
        return component
    
    for i in range(n):
        if not visited[i]:
            components.append(dfs(i))
    
    # Calculate the number of independent sets for each component
    def independent_sets_count(size: int) -> int:
        if size == 0:
            return 1
        if size == 1:
            return 2
        a, b = 1, 2
        for _ in range(2, size + 1):
            a, b = b, (a + b) % MOD
        return b
    
    total_sets = 1
    for component in components:
        total_sets = total_sets * independent_sets_count(len(component)) % MOD
    
    return total_sets

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    robots = [(int(data[2*i+1]), int(data[2*i+2])) for i in range(n)]
    
    result = count_independent_sets(n, robots)
    print(result)

if __name__ == "__main__":
    main()