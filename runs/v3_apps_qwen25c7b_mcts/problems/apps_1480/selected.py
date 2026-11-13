def eliminate_children(n, k, steps):
    children = list(range(1, n + 1))
    leader_index = 0
    
    def find_next_eliminated(index, step):
        nonlocal leader_index
        index = (index + step) % len(children)
        eliminated_child = children.pop(index)
        leader_index = index
        return eliminated_child
    
    result = []
    for step in steps:
        result.append(find_next_eliminated(leader_index, step))
    
    return result

# Input reading
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])
steps = list(map(int, data[2:]))

# Output the result
print(' '.join(map(str, eliminate_children(n, k, steps))))