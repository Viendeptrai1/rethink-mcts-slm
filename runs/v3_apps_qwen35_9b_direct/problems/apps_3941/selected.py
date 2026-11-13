import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    iterator = iter(data)

    try:
        n = int(next(iterator))
        m = int(next(iterator))
    except StopIteration:
        return

    r = [0] * (n + 1)
    for i in range(1, n + 1):
        r[i] = int(next(iterator))

    # Adjacency list: switch -> list of rooms
    switch_rooms = [[] for _ in range(m + 1)]
    # Reverse mapping: room -> list of switches
    room_switches = [[] for _ in range(n + 1)]

    for i in range(1, m + 1):
        x = int(next(iterator))
        rooms = []
        for _ in range(x):
            room = int(next(iterator))
            rooms.append(room)
        switch_rooms[i] = rooms
        for room in rooms:
            room_switches[room].append(i)

    # We need to determine if there exists a configuration of switches (s_1, ..., s_m) in {0, 1}
    # such that for every room j, the final state is 1 (unlocked).
    # Let initial state be r[j].
    # Let s[k] be 1 if switch k is toggled, 0 otherwise.
    # Final state of room j = r[j] XOR (sum of s[k] for all k controlling j) mod 2.
    # We require: r[j] XOR (sum of s[k]) = 1  =>  (sum of s[k]) = 1 XOR r[j].
    # Let target[j] = 1 XOR r[j].
    # So for each room j, the sum of switches controlling it must have parity equal to target[j].

    # Build equations:
    # For each room j, we have an equation: sum(s[k] for k in room_switches[j]) % 2 = target[j]
    # This is a system of linear equations over GF(2).
    # Variables: s_1, ..., s_m
    # Equations: one per room (n equations)

    # We can use Gaussian elimination.
    # Matrix size: n rows x (m+1) columns (last column is the constant term).
    # However, n and m are up to 10^5, so O(n*m) is too slow.
    # But note: each room has exactly 2 switches. So each equation has exactly 2 variables.
    # This is a system where each equation is of the form: s[a] + s[b] = c (mod 2).
    # This structure allows us to solve it efficiently using a graph approach or optimized Gaussian elimination.
    # Actually, since each equation involves exactly 2 variables, we can view this as a graph problem.
    # Variables are nodes, equations are edges between the two switches involved in that room.
    # The value of the edge is the required parity (target[j]).
    # We need to assign values to nodes such that for every edge (u, v) with weight w, s[u] + s[v] = w (mod 2).
    # This is possible if and only if for every connected component, the constraints are consistent.
    # In a connected component, once we fix the value of one node, all others are determined.
    # We can pick an arbitrary node, set it to 0, propagate, and check for contradictions.
    # If a contradiction is found (i.e., we reach a node with a conflicting required value), then NO.
    # If no contradiction in any component, then YES.

    # Steps:
    # 1. Build a graph where nodes are switches (1..m).
    # 2. For each room j, add an edge between the two switches controlling it. The edge has a weight = target[j].
    #    Note: target[j] = 1 ^ r[j].
    # 3. Iterate over all switches. If a switch is not visited, start a BFS/DFS to traverse its component.
    #    - Assign a tentative value to the starting switch (say 0).
    #    - Propagate: if we have an edge (u, v) with weight w, and we know s[u], then s[v] must be s[u] ^ w.
    #    - If we encounter a visited node v with a previously assigned value, check if the new required value matches.
    #      If not, return "NO".
    # 4. If all components are consistent, return "YES".

    # Build graph: adj[u] = [(v, weight), ...]
    adj = [[] for _ in range(m + 1)]
    target = [0] * (n + 1)
    for j in range(1, n + 1):
        t = 1 ^ r[j]
        target[j] = t
        # Get the two switches for room j
        sw1, sw2 = room_switches[j]
        # Edge between sw1 and sw2 with weight t
        adj[sw1].append((sw2, t))
        adj[sw2].append((sw1, t))

    visited = [False] * (m + 1)
    assigned = [0] * (m + 1)  # stores the value of the switch (0 or 1)

    for i in range(1, m + 1):
        if not visited[i]:
            # Start BFS/DFS from i
            stack = [(i, 0)]  # (node, value)
            visited[i] = True
            assigned[i] = 0
            
            while stack:
                u, val = stack.pop()
                
                for v, w in adj[u]:
                    # Required: s[u] + s[v] = w (mod 2) => s[v] = s[u] ^ w
                    required_v = val ^ w
                    
                    if not visited[v]:
                        visited[v] = True
                        assigned[v] = required_v
                        stack.append((v, required_v))
                    else:
                        if assigned[v] != required_v:
                            print("NO")
                            return

    print("YES")

if __name__ == "__main__":
    solve()