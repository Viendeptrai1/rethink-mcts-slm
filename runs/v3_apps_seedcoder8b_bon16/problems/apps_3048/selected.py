from sys import stdin, stdout
from collections import defaultdict, deque

def count_optimal_paths_of_length_2(N, edges):
    # Create an adjacency list for the tree
    tree = defaultdict(list)
    for u, v in edges:
        tree[u].append(v)
        tree[v].append(u)

    # Function to perform BFS and count nodes at distance 2
    def bfs_count_dist_2(start_node):
        visited = [-1] * (N + 1)
        queue = deque([(start_node, 0)])
        visited[start_node] = 0
        count = 0
        while queue:
            node, dist = queue.popleft()
            for neighbor in tree[node]:
                if visited[neighbor] == -1:  # Not visited
                    visited[neighbor] = dist + 1
                    if visited[neighbor] == 2:
                        count += 1
                    queue.append((neighbor, dist + 1))
        return count

    total_paths = 0
    # For each node, perform BFS and sum up paths of length 2
    for node in range(1, N + 1):
        total_paths += bfs_count_dist_2(node)

    # Since each path is counted twice (once from each end), divide by 2
    return total_paths // 2

def main():
    input = stdin.readline
    print = stdout.write
    N = int(input().strip())
    edges = [tuple(map(int, input().strip().split())) for _ in range(N - 1)]
    result = count_optimal_paths_of_length_2(N, edges)
    print(f"{result}\n")

if __name__ == "__main__":
    main()