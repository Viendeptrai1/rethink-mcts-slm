def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    a = list(map(int, data[2:2+k]))
    
    children = list(range(1, n + 1))
    leader_index = 0
    
    for step in range(k):
        a_i = a[step]
        # Calculate the index of the child to eliminate
        eliminate_index = (leader_index + a_i) % len(children)
        # Print the child to be eliminated
        print(children[eliminate_index], end=' ')
        # Remove the eliminated child
        children.pop(eliminate_index)
        # Update the leader index
        leader_index = eliminate_index if eliminate_index < len(children) else 0

if __name__ == "__main__":
    solve()