import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    idx = 0
    t = int(data[idx])
    idx += 1
    
    results = []
    
    for _ in range(t):
        n = int(data[idx])
        idx += 1
        s = data[idx]
        idx += 1
        
        # Convert string to a list of integers for easier processing
        # '>' -> 1 (clockwise)
        # '<' -> -1 (anticlockwise)
        # '-' -> 0 (off)
        moves = []
        for char in s:
            if char == '>':
                moves.append(1)
            elif char == '<':
                moves.append(-1)
            else:
                moves.append(0)
        
        # A room is returnable if there is a cycle reachable from it that includes it.
        # In this circular graph, a room i is returnable if:
        # 1. It can reach a cycle.
        # 2. From that cycle, it can reach itself.
        #
        # Key Insight:
        # - If there is any '-' (off) belt, the entire circle becomes strongly connected 
        #   because you can traverse the '-' belt in both directions, effectively merging 
        #   the clockwise and anticlockwise paths into one large component where everyone 
        #   can reach everyone else (provided the graph is connected, which it is in a circle 
        #   with at least one bidirectional edge).
        #   Wait, let's re-verify. If there is one '-', say between i and i+1.
        #   You can go i -> i+1 and i+1 -> i.
        #   Can you go from any node to any other?
        #   Yes. From any node u, you can follow the directed edges until you hit the '-' belt 
        #   or complete a loop. Since it's a circle, you will eventually hit the '-' belt.
        #   Once at the '-' belt, you can cross it. Then you can continue.
        #   Actually, simpler logic:
        #   If there is at least one '-', the whole graph is one strongly connected component?
        #   Not necessarily if the directed edges form a barrier that prevents reaching the '-' 
        #   from some nodes? No, in a circle, you can always go around.
        #   However, consider: > > > - < < <
        #   The '-' allows crossing. But can we go from the right side of '-' to the left?
        #   Right side has '<' pointing left. Left side has '>' pointing right.
        #   So yes, we can go right -> left via '<' and left -> right via '>' and '-'.
        #   What if we have > > > > and no '-'? Then it's a simple cycle, everyone is returnable.
        #   What if we have < < < < and no '-'? Simple cycle, everyone returnable.
        #   What if we have > > < < (no '-')? 
        #   0->1->2, 3->2, 1->0? No.
        #   Let's trace > > < < (n=4):
        #   0->1, 1->2, 2<-3 (so 3->2), 3<-0 (so 0->3? No, s[3] is '<', so 3->2? No.
        #   s[i] connects i and (i+1)%n.
        #   s[0]='>' : 0->1
        #   s[1]='>' : 1->2
        #   s[2]='<' : 3->2
        #   s[3]='<' : 0->3? No. s[3] connects 3 and 0. '<' means (3+1)%4 -> 3, i.e., 0->3.
        #   Edges: 0->1, 1->2, 3->2, 0->3.
        #   Paths: 0->1->2. 0->3->2.
        #   Can 2 go anywhere? No outgoing from 2.
        #   Can 1 go to 0? No.
        #   Can 3 go to 0? No.
        #   So only 0 is returnable? 0->1->2 (stuck). 0->3->2 (stuck).
        #   Wait, "returnable" means leave and come back.
        #   If 0 goes to 1, can it come back? No.
        #   If 0 goes to 3, can it come back? No.
        #   So 0 is NOT returnable?
        #   Let's re-read the definition. "leave its room and come back to it later".
        #   This implies a cycle must exist that the snake can enter.
        #   In > > < <, there are no cycles. 0->1->2 (dead end). 0->3->2 (dead end).
        #   So count = 0.
        #
        #   General Logic:
        #   1. If there is at least one '-', the entire circle is strongly connected.
        #      Why? Because the '-' acts as a bridge. Even if other edges are directed, 
        #      the presence of a bidirectional edge in a cycle usually makes the whole thing 
        #      one component IF the directed edges don't form a cut that isolates parts.
        #      But in a simple cycle graph, removing one edge leaves a line. Adding a bidirectional 
        #      edge back makes it a cycle with a "double" link.
        #      Actually, if there is a '-', can we always go from any node to any other?
        #      Suppose we have > > > - < < <.
        #      Nodes 0,1,2,3,4,5,6. '-' at 3 (between 3 and 4).
        #      0->1->2->3. At 3, we can go to 4 (via '-') or 3->2 (via '>').
        #      From 4, we have 4->3 (via '<')? No, s[4]='<', so 5->4.
        #      So from 4, we can only go to 3? No, s[4] connects 4 and 5. '<' means 5->4.
        #      So 4 has no outgoing edge to 5. Does 4 have outgoing to 3? Yes, via '-'.
        #      So 4->3. Then 3->4. So 3 and 4 form a cycle.
        #      Can we reach 3 from 0? Yes (0->1->2->3).
        #      Can we reach 0 from 3? 3->4->3... stuck in 3-4 loop?
        #      Wait, if 3 and 4 form a loop, and 0 can reach them, can they reach 0?
        #      From 3, we can go to 2 (via '>'). 2->1->0. Yes!
        #      So 0 is reachable from 3.
        #      It seems if there is a '-', the whole graph is strongly connected.
        #      Proof sketch: The '-' edge (u, v) allows u->v and v->u.
        #      Any node x can reach u or v by following the directed edges (since it's a circle, 
        #      you can go clockwise or anticlockwise until you hit the '-' or a node that can reach it).
        #      Actually, simpler: In a circle, if there is a bidirectional edge, the graph is 
        #      strongly connected. Because you can traverse the circle in both directions using 
        #      the bidirectional edge to switch direction if needed, and the directed edges 
        #      just guide you.
        #      Wait, what if all other edges are blocking?
        #      Example: > > > - < < <
        #      We saw 0->...->3->4->3->2->...->0. It works.
        #      Is there a counterexample?
        #      Suppose > > > - < < < < (n=7).
        #      It seems robust. If there is a '-', count = n.
        #
        #   2. If there are no '-', then all edges are directed.
        #      The graph is a collection of directed edges on a circle.
        #      A cycle exists if and only if all edges in the circle are in the same direction.
        #      If we have a mix of '>' and '<', then there is no cycle.
        #      Why? Because to have a cycle in a directed graph that is a subgraph of a circle, 
        #      you must traverse the circle completely in one direction. If you encounter an edge 
        #      pointing the opposite way, you cannot cross it, breaking the cycle.
        #      So if there is no '-' and there is at least one '>' and at least one '<', 
        #      then there are NO cycles. Count = 0.
        #      If all are '>' or all are '<', then there is one big cycle. Count = n.
        
        if '-' in s:
            results.append(n)
        else:
            # No '-'
            if '>' in s and '<' in s:
                results.append(0)
            else:
                # All same direction
                results.append(n)
    
    print('\n'.join(map(str, results)))

if __name__ == '__main__':
    solve()