import sys

# Increase recursion depth for deep DFS traversals if necessary
sys.setrecursionlimit(200000)

def solve():
    # Read all input from stdin at once
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        n = int(next(iterator))
        m = int(next(iterator))
        
        # Read initial door states
        # r_i is 0 (locked) or 1 (unlocked)
        # We will store them in a 0-indexed list
        initial_state = []
        for _ in range(n):
            initial_state.append(int(next(iterator)))
            
        # Build adjacency list for the graph where nodes are switches (0 to m-1)
        # Each door connects two switches.
        # We need to store the constraint type for each edge.
        # Constraint: 
        # If door is locked (0): switches must be different (one 0, one 1) -> XOR sum = 1
        # If door is unlocked (1): switches must be same (both 0 or both 1) -> XOR sum = 0
        # Let switch state be s_i (0 or 1).
        # Condition: s_u ^ s_v = (1 if door_locked else 0)
        
        adj = [[] for _ in range(m)]
        
        # We need to map room indices (1-based) to the two switches controlling them.
        # Since we process switches line by line, we can't easily build the reverse map without storing.
        # Instead, let's store the edges as we read the switch configurations.
        # But we need to know which two switches control a specific room to build the graph.
        # The problem says: "each door is controlled by exactly two switches".
        # Input gives us for each switch, which rooms it controls.
        # We can create a list of lists `room_to_switches` of size n+1.
        
        room_to_switches = [[] for _ in range(n + 1)]
        
        for switch_idx in range(m):
            try:
                count = int(next(iterator))
                rooms = []
                for _ in range(count):
                    rooms.append(int(next(iterator)))
                
                for room in rooms:
                    room_to_switches[room].append(switch_idx)
            except StopIteration:
                break
        
        # Now build the graph
        # Nodes: 0 to m-1 (switches)
        # Edges: derived from rooms. Each room adds an edge between its two controlling switches.
        
        for room in range(1, n + 1):
            switches = room_to_switches[room]
            if len(switches) != 2:
                # This should not happen based on problem statement
                continue
            
            u, v = switches[0], switches[1]
            door_state = initial_state[room - 1]
            
            # Constraint: s_u ^ s_v = (1 if door_state == 0 else 0)
            # If door is locked (0), we need s_u != s_v => s_u ^ s_v = 1
            # If door is unlocked (1), we need s_u == s_v => s_u ^ s_v = 0
            weight = 1 if door_state == 0 else 0
            
            adj[u].append((v, weight))
            adj[v].append((u, weight))
            
        # Check for consistency using BFS/DFS (2-coloring with weights)
        # We need to assign a value (0 or 1) to each switch such that for every edge (u, v) with weight w:
        # val[u] ^ val[v] == w
        
        visited = [False] * m
        color = [-1] * m
        possible = True
        
        for i in range(m):
            if not visited[i]:
                # Start BFS/DFS from this component
                # Arbitrarily set color[i] = 0
                color[i] = 0
                visited[i] = True
                stack = [i]
                
                while stack:
                    u = stack.pop()
                    u_color = color[u]
                    
                    for v, w in adj[u]:
                        if not visited[v]:
                            visited[v] = True
                            # Determine required color for v
                            # color[u] ^ color[v] = w  =>  color[v] = color[u] ^ w
                            color[v] = u_color ^ w
                            stack.append(v)
                        else:
                            # Check consistency
                            if color[v] != (u_color ^ w):
                                possible = False
                                break
                    if not possible:
                        break
                if not possible:
                    break
        
        if possible:
            print("YES")
        else:
            print("NO")
            
    except StopIteration:
        pass

if __name__ == "__main__":
    solve()