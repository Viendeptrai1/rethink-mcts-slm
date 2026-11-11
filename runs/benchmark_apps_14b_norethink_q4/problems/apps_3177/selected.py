from collections import deque

def min_swaps_to_order(N, M, initial_permutation, allowed_swaps):
    # Convert initial permutation to 0-indexed for easier manipulation
    initial_permutation = [x - 1 for x in initial_permutation]
    
    # Create a dictionary to store the allowed swaps for quick lookup
    swap_dict = {}
    for A, B in allowed_swaps:
        if A not in swap_dict:
            swap_dict[A] = set()
        if B not in swap_dict:
            swap_dict[B] = set()
        swap_dict[A].add(B)
        swap_dict[B].add(A)
    
    # Define the target permutation (0-indexed)
    target_permutation = list(range(N))
    
    # Initialize BFS queue and visited set
    queue = deque([(initial_permutation, 0)])  # (current permutation, number of swaps)
    visited = set()
    visited.add(tuple(initial_permutation))
    
    while queue:
        current_permutation, swaps = queue.popleft()
        
        # If we reached the target permutation, return the number of swaps
        if current_permutation == target_permutation:
            return swaps
        
        # Generate all possible next permutations by performing allowed swaps
        for i in range(N):
            if i + 1 in swap_dict:
                for j in swap_dict[i + 1]:
                    next_permutation = current_permutation[:]
                    next_permutation[i], next_permutation[j - 1] = next_permutation[j - 1], next_permutation[i]
                    
                    if tuple(next_permutation) not in visited:
                        visited.add(tuple(next_permutation))
                        queue.append((next_permutation, swaps + 1))

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    M = int(data[1])
    initial_permutation = list(map(int, data[2:2+N]))
    allowed_swaps = [(int(data[2+N+2*i]), int(data[2+N+2*i+1])) for i in range(M)]
    
    result = min_swaps_to_order(N, M, initial_permutation, allowed_swaps)
    print(result)