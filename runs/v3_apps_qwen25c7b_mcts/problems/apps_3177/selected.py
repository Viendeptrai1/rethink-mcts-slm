from collections import deque

def min_swaps_to_sort(n, m, perm, swaps):
    target = list(range(1, n + 1))
    visited = set()
    queue = deque([(perm, 0)])
    
    while queue:
        current_perm, swaps_count = queue.popleft()
        
        if current_perm == target:
            return swaps_count
        
        for i, j in swaps:
            new_perm = current_perm[:]
            new_perm[i - 1], new_perm[j - 1] = new_perm[j - 1], new_perm[i - 1]
            
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
    perm = list(map(int, data[2:2+n]))
    swaps = [(int(data[2+n+2*i]), int(data[2+n+2*i+1])) for i in range(m)]
    
    result = min_swaps_to_sort(n, m, perm, swaps)
    print(result)