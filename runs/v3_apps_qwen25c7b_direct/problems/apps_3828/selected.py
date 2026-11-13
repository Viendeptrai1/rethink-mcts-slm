def min_actions_to_sort(n, p):
    sorted_p = sorted(p)
    index_map = {v: i for i, v in enumerate(sorted_p)}
    current_index = [index_map[p[i]] for i in range(n)]
    
    def find_min_swaps(arr):
        visited = [False] * len(arr)
        swaps = 0
        
        for i in range(len(arr)):
            if visited[i] or arr[i] == i:
                continue
            
            cycle_size = 0
            x = i
            
            while not visited[x]:
                visited[x] = True
                x = arr[x]
                cycle_size += 1
            
            if cycle_size > 0:
                swaps += (cycle_size - 1)
        
        return swaps
    
    return find_min_swaps(current_index)

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
p = list(map(int, data[1:]))

print(min_actions_to_sort(n, p))