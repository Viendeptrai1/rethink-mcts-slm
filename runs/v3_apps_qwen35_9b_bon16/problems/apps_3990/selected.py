import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        n = int(next(iterator))
        m = int(next(iterator))
    except StopIteration:
        return

    # Adjacency set for railways
    railways = set()
    for _ in range(m):
        u = int(next(iterator))
        v = int(next(iterator))
        railways.add((u, v))
        railways.add((v, u))

    # Special case: if there is a direct railway between 1 and n
    # Train takes 1 hour, Bus needs at least 2 hours (1 -> other -> n) because no direct road.
    # But wait, if there is a direct railway, there is NO direct road.
    # Train: 1 -> n (1 hour)
    # Bus: must go via some intermediate node. Minimum 2 hours.
    # So answer is max(1, 2) = 2? 
    # Let's re-evaluate logic carefully.
    
    # Case 1: Direct railway exists between 1 and n.
    # Train uses railway: 1 -> n (1 hour).
    # Bus cannot use direct road. Must take at least 2 steps: 1 -> x -> n.
    # Is it possible for Bus to take 2 steps? Only if there exists an x such that (1,x) is road and (x,n) is road.
    # (1,x) is road iff (1,x) is NOT railway.
    # (x,n) is road iff (x,n) is NOT railway.
    # Since n >= 2, there is at least one node. If n=2, nodes are 1,2. No intermediate x. Bus cannot move?
    # If n=2 and railway (1,2) exists:
    #   Train: 1->2 (1h).
    #   Bus: No other towns. Cannot move. Output -1.
    # If n>2 and railway (1,n) exists:
    #   Train: 1->n (1h).
    #   Bus: Needs path of length 2. Any x != 1, x != n works if (1,x) and (x,n) are roads.
    #   Since (1,n) is railway, (1,n) is not road.
    #   We need x such that (1,x) not in railways and (x,n) not in railways.
    #   If such x exists, bus time = 2. Max(1, 2) = 2.
    #   If no such x exists, bus cannot reach? Actually bus might need more steps but shortest path would be >=2.
    #   Wait, if no x satisfies the condition for 2 steps, can bus take 3 steps? 
    #   Actually, if (1,n) is railway, then for any x, either (1,x) is railway OR (x,n) is railway? Not necessarily.
    #   But we want MINIMUM time. If bus can reach in 2, answer is 2. If not, maybe 3?
    #   However, consider the graph complement.
    #   If (1,n) is edge in G (railways), then (1,n) is NOT edge in G' (roads).
    #   Distance in G' from 1 to n.
    #   If dist_G'(1, n) == 2, then answer 2.
    #   If dist_G'(1, n) > 2, then answer > 2.
    #   BUT, there is a simpler logic often used in this problem:
    #   If (1,n) is railway:
    #     Train time = 1.
    #     Bus time = shortest path in road graph.
    #     If road graph has no path, -1.
    #     Else, result = max(1, dist).
    #   If (1,n) is NOT railway:
    #     Train time = shortest path in railway graph.
    #     Bus time = 1 (direct road).
    #     If railway graph has no path, -1.
    #     Else, result = max(dist, 1).

    # Let's implement BFS for both cases.
    # Build road graph implicitly or explicitly? n is small (400), explicit is fine.
    
    # Build adjacency list for roads
    road_adj = [[] for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            if (i, j) not in railways:
                road_adj[i].append(j)
                road_adj[j].append(i)
    
    # Build adjacency list for railways
    rail_adj = [[] for _ in range(n + 1)]
    for u, v in railways:
        rail_adj[u].append(v)
        rail_adj[v].append(u)

    def bfs(start, end, adj_list):
        if start == end:
            return 0
        dist = [-1] * (n + 1)
        dist[start] = 0
        queue = [start]
        idx = 0
        while idx < len(queue):
            u = queue[idx]
            idx += 1
            if u == end:
                return dist[u]
            for v in adj_list[u]:
                if dist[v] == -1:
                    dist[v] = dist[u] + 1
                    queue.append(v)
        return -1

    has_direct_rail = (1, n) in railways

    if has_direct_rail:
        # Train uses rail: 1 hop
        train_time = 1
        
        # Bus uses roads. Check connectivity from 1 to n in road graph.
        bus_time = bfs(1, n, road_adj)
        
        if bus_time == -1:
            print("-1")
        else:
            print(max(train_time, bus_time))
    else:
        # Bus uses road: 1 hop
        bus_time = 1
        
        # Train uses rails. Check connectivity from 1 to n in rail graph.
        train_time = bfs(1, n, rail_adj)
        
        if train_time == -1:
            print("-1")
        else:
            print(max(bus_time, train_time))

if __name__ == "__main__":
    solve()