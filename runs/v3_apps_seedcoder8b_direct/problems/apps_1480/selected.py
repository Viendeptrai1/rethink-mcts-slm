def solve_counting_out_game():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    a = list(map(int, data[2:2+k]))
    
    children = list(range(1, n + 1))
    leader_index = 0
    
    result = []
    
    for i in range(k):
        step_count = a[i] % n
        leader_index = (leader_index + step_count) % n
        eliminated_child = children.pop(leader_index)
        result.append(eliminated_child)
        if leader_index == len(children):
            leader_index = 0
    
    print(" ".join(map(str, result)))