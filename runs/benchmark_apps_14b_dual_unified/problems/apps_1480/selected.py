def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    
    children = list(range(1, n + 1))
    leader_index = 0
    eliminated_children = []
    
    for i in range(k):
        ai = int(data[2 + i])
        # Calculate the index of the child to be eliminated
        eliminate_index = (leader_index + ai) % len(children)
        eliminated_children.append(children[eliminate_index])
        
        # Remove the eliminated child from the list
        children.pop(eliminate_index)
        
        # Update the leader index
        leader_index = eliminate_index % len(children)
    
    # Print the result
    print(' '.join(map(str, eliminated_children)))

if __name__ == "__main__":
    main()