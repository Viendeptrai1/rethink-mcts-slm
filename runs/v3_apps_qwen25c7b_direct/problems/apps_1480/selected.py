def count_out_game(n, k, a):
    children = list(range(1, n + 1))
    leader_index = 0
    
    for i in range(k):
        eliminate_index = (leader_index + a[i] - 1) % len(children)
        eliminated_child = children.pop(eliminate_index)
        leader_index = eliminate_index
        
        print(eliminated_child)

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])
a = list(map(int, data[2:]))

count_out_game(n, k, a)