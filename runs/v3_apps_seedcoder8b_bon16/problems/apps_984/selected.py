def count_search_failures(n, tree):
    from collections import defaultdict, deque

    # Build the tree from input
    nodes = [None] * n
    for i in range(n):
        v, l, r = tree[i]
        nodes[i] = (v, l, r)
    
    def find_failures(start_value, start_index):
        if start_index == -1:
            return 0
        
        value, left_index, right_index = nodes[start_index]
        queue = deque([(start_index, start_value)])
        failures = 0
        
        while queue:
            current_index, target = queue.popleft()
            current_value, left_child, right_child = nodes[current_index]
            
            if current_value == target:
                continue
            elif current_value > target:
                if left_child == -1:
                    failures += 1
                else:
                    queue.append((left_child, target))
            else:
                if right_child == -1:
                    failures += 1
                else:
                    queue.append((right_child, target))
        
        return failures

    total_failures = 0
    visited = set()

    for i in range(n):
        value, _, _ = nodes[i]
        if value not in visited:
            visited.add(value)
            total_failures += find_failures(value, i)
    
    return total_failures

# Read input
import sys
input = sys.stdin.read
data = input().strip().split('\n')
n = int(data[0].strip())
tree = [tuple(map(int, line.strip().split())) for line in data[1:]]

# Calculate and print the result
result = count_search_failures(n, tree)
print(result)