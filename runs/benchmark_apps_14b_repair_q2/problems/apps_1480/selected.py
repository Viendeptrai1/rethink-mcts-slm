def main():
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
        count_out = a[step]
        index_to_eliminate = (leader_index + count_out) % len(children)
        eliminated_child = children.pop(index_to_eliminate)
        result.append(eliminated_child)
        leader_index = index_to_eliminate % len(children)
    
    print(" ".join(map(str, result)))

if __name__ == "__main__":
    main()