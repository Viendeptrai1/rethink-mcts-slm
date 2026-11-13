import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    idx = 0
    
    n = int(data[idx]); idx += 1
    m = int(data[idx]); idx += 1
    
    # Current state of doors: 0 for locked, 1 for unlocked
    # We need final state to be 1 for all.
    # Let s_i be the state of switch i (0 or 1).
    # Let initial state of room j be R[j].
    # Final state of room j = (R[j] + sum(s_k for all k controlling j)) % 2
    # We want Final state = 1.
    # So: (R[j] + sum(s_k)) % 2 = 1  =>  sum(s_k) % 2 = (1 - R[j]) % 2
    # Let target[j] = (1 - R[j]) % 2. This is what the sum of switches controlling room j must equal modulo 2.
    
    r_initial = []
    for _ in range(n):
        r_initial.append(int(data[idx])); idx += 1
        
    # Build adjacency list: room -> list of switches controlling it
    # Since each door is controlled by exactly two switches, this list will always have length 2.
    room_switches = [[] for _ in range(n + 1)]
    
    for i in range(1, m + 1):
        x = int(data[idx]); idx += 1
        rooms = []
        for _ in range(x):
            rooms.append(int(data[idx])); idx += 1
        for room in rooms:
            room_switches[room].append(i)
            
    # Determine required parity for the sum of switches for each room
    # target[j] = 1 if we need to toggle an odd number of times, 0 if even
    target = [0] * (n + 1)
    for j in range(1, n + 1):
        if r_initial[j-1] == 0:
            # Currently locked, need odd toggles to become unlocked
            target[j] = 1
        else:
            # Currently unlocked, need even toggles to stay unlocked
            target[j] = 0
            
    # Each switch i controls some rooms. Let's denote the set of rooms controlled by switch i as S_i.
    # The constraint for room j is: sum_{k in S_j} s_k = target[j] (mod 2)
    # Since each room is in exactly 2 switches, we have a system of linear equations over GF(2).
    # Specifically, for each room j, if it is controlled by switches u and v:
    # s_u + s_v = target[j] (mod 2)
    # This implies s_u = s_v + target[j] (mod 2).
    # This means the relationship between s_u and s_v is fixed by the room j.
    # We can model this as a graph where nodes are switches (1..m).
    # For each room j controlled by u and v:
    #   If target[j] == 0, then s_u must equal s_v.
    #   If target[j] == 1, then s_u must be different from s_v.
    # We need to check if there exists an assignment of s_i in {0, 1} satisfying all these constraints.
    # This is equivalent to checking if the graph is bipartite if we treat "same" as no edge and "different" as edge?
    # Actually, let's build a graph where edges represent constraints.
    # Nodes: switches 1..m
    # Edges: For each room j (controlled by u, v):
    #   Add an edge between u and v with weight = target[j].
    #   Weight 0 means s_u == s_v.
    #   Weight 1 means s_u != s_v.
    # We can use BFS/DFS to assign values relative to a starting node and check for contradictions.
    # If a contradiction is found (e.g., s_u must be 0 and 1), then NO.
    # If no contradiction, then YES.
    
    # Graph representation: adj[u] = [(v, weight), ...]
    adj = [[] for _ in range(m + 1)]
    
    for j in range(1, n + 1):
        switches = room_switches[j]
        if len(switches) != 2:
            # Should not happen based on problem statement
            continue
        u, v = switches
        w = target[j]
        adj[u].append((v, w))
        adj[v].append((u, w))
        
    visited = [False] * (m + 1)
    val = [0] * (m + 1) # val[u] stores the required value relative to some root (0 or 1)
    
    for i in range(1, m + 1):
        if not visited[i]:
            # Start a new component
            q = [i]
            visited[i] = True
            val[i] = 0 # Arbitrarily set root to 0
            possible = True
            
            idx_q = 0
            while idx_q < len(q):
                u = q[idx_q]
                idx_q += 1
                
                for v, w in adj[u]:
                    if not visited[v]:
                        visited[v] = True
                        # If w=0, s_v = s_u. If w=1, s_v = 1 - s_u.
                        val[v] = val[u] ^ w
                        q.append(v)
                    else:
                        # Check consistency
                        expected = val[u] ^ w
                        if val[v] != expected:
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

if __name__ == "__main__":
    solve()