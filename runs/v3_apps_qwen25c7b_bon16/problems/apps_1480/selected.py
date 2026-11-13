import sys

def play_game(n, k, steps):
    children = list(range(1, n + 1))
    leader_index = 0
    
    eliminated_children = []
    
    for step in steps:
        eliminate_index = (leader_index + step) % len(children)
        eliminated_child = children.pop(eliminate_index)
        eliminated_children.append(eliminated_child)
        leader_index = eliminate_index % len(children)
    
    return eliminated_children

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    steps = list(map(int, data[2:]))
    
    result = play_game(n, k, steps)
    for child in result:
        print(child)