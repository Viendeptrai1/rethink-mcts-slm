def find_children_to_eliminate(n, k, a):
    children = list(range(1, n + 1))
    leader_index = 0
    result = []

    for step in range(k):
        count = a[step] % len(children)
        leader_index = (leader_index + count) % len(children)
        eliminated_child = children.pop(leader_index)
        result.append(eliminated_child)

    return result

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    a = list(map(int, data[2:2 + k]))
    
    result = find_children_to_eliminate(n, k, a)
    print(" ".join(map(str, result)))