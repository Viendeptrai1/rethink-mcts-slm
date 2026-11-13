import sys
from collections import defaultdict, deque

MOD = 1_000_000_007

def count_valid_rankings(names):
    # Sort names lexicographically
    names.sort()
    
    # Create a graph and in-degree count
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    
    # Create a prefix map to store the first occurrence of each prefix
    prefix_map = {}
    
    for i, name in enumerate(names):
        prefix = ""
        for char in name:
            prefix += char
            if prefix in prefix_map:
                # Add an edge from the first occurrence of this prefix to the current name
                prev_index = prefix_map[prefix]
                if prev_index != i:
                    graph[prev_index].append(i)
                    in_degree[i] += 1
            else:
                prefix_map[prefix] = i
    
    # Topological sort using Kahn's algorithm
    queue = deque()
    for i in range(len(names)):
        if in_degree[i] == 0:
            queue.append(i)
    
    dp = [0] * len(names)
    for i in range(len(names)):
        dp[i] = 1
    
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            dp[neighbor] = (dp[neighbor] + dp[node]) % MOD
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Sum up all possible orderings
    return sum(dp) % MOD

def main():
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    names = data[1:N+1]
    
    result = count_valid_rankings(names)
    print(result)

if __name__ == "__main__":
    main()