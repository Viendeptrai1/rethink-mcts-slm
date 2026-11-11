def find_eliminated_child(n, k, steps):
    children = list(range(1, n + 1))
    leader_index = 0
    result = []

    for step in steps:
        leader_index = (leader_index + step) % len(children)
        eliminated_child = children.pop(leader_index)
        result.append(eliminated_child)
        if leader_index == len(children):
            leader_index = 0

    return result

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    steps = list(map(int, data[2:2+k]))
    
    result = find_eliminated_child(n, k, steps)
    print(" ".join(map(str, result)))

if __name__ == "__main__":
    main()