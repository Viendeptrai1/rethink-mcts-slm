def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    
    a = list(map(int, data[2:2+k]))
    
    children = list(range(1, n + 1))
    leader_index = 0
    result = []
    
    for step in range(k):
        count = a[step]
        index_to_remove = (leader_index + count) % len(children)
        eliminated_child = children[index_to_remove]
        result.append(eliminated_child)
        
        children.pop(index_to_remove)
        if index_to_remove == len(children):
            leader_index = 0
        else:
            leader_index = index_to_remove
    
    print(" ".join(map(str, result)))

solve()