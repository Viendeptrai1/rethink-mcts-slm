import sys
from collections import defaultdict, deque

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    f = list(map(int, data[1:]))
    
    # Create a graph to represent the friendships
    graph = defaultdict(list)
    unassigned = []
    
    for i in range(n):
        if f[i] == 0:
            unassigned.append(i)
        else:
            graph[f[i] - 1].append(i)
    
    # Assign gifts to unassigned friends
    result = [0] * n
    for i in range(n):
        if f[i] != 0:
            result[i] = f[i]
    
    # Process unassigned friends
    for u in unassigned:
        if not graph[u]:
            # If there's no cycle, just assign the next available friend
            for v in range(n):
                if result[v] == 0:
                    result[v] = u + 1
                    break
        else:
            # If there's a cycle, we need to break it
            cycle = []
            visited = set()
            x = u
            while x not in visited:
                visited.add(x)
                cycle.append(x)
                x = graph[x][0]
            
            # Break the cycle by assigning the last friend in the cycle to the first
            result[cycle[-1]] = cycle[0] + 1
            
            # Assign the rest of the cycle
            for i in range(len(cycle) - 1):
                result[cycle[i]] = cycle[i + 1] + 1
    
    # Print the result
    print(" ".join(map(str, result)))

if __name__ == "__main__":
    main()