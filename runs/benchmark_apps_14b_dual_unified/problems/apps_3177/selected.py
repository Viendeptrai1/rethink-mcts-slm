from collections import deque

def min_swaps_to_sort(n, m, permutation, swaps):
    # Create adjacency list for the graph
    graph = {i: [] for i in range(1, n + 1)}
    for a, b in swaps:
        graph[a].append(b)
        graph[b].append(a)
    
    # Function to get the index of a value in the current permutation
    def get_index(value):
        return permutation.index(value) + 1
    
    # BFS to find the minimum number of swaps
    queue = deque([(permutation, 0)])  # (current permutation, number of swaps)
    visited = set()
    visited.add(tuple(permutation))
    
    while queue:
        current_perm, swaps_count = queue.popleft()
        
        # Check if the current permutation is sorted
        if current_perm == list(range(1, n + 1)):
            return swaps_count
        
        # Try all possible swaps
        for i in range(n):
            for j in range(i + 1, n):
                if (current_perm[i], current_perm[j]) in swaps or (current_perm[j], current_perm[i]) in swaps:
                    # Perform the swap
                    new_perm = current_perm[:]
                    new_perm[i], new_perm[j] = new_perm[j], new_perm[i]
                    
                    # If the new permutation hasn't been visited, add it to the queue
                    if tuple(new_perm) not in visited:
                        visited.add(tuple(new_perm))
                        queue.append((new_perm, swaps_count + 1))

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    permutation = list(map(int, data[2:2+n]))
    swaps = [(int(data[2+n+2*i]), int(data[2+n+2*i+1])) for i in range(m)]
    
    result = min_swaps_to_sort(n, m, permutation, swaps)
    print(result)