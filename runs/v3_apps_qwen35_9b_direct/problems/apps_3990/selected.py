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
    railway_adj = [set() for _ in range(n + 1)]
    for _ in range(m):
        u = int(next(iterator))
        v = int(next(iterator))
        railway_adj[u].add(v)
        railway_adj[v].add(u)

    # Calculate shortest path for train (railways) from 1 to n
    # BFS
    def bfs_rail():
        if n == 1:
            return 0
        dist = [-1] * (n + 1)
        dist[1] = 0
        queue = [1]
        while queue:
            u = queue.pop(0)
            if u == n:
                return dist[u]
            for v in railway_adj[u]:
                if dist[v] == -1:
                    dist[v] = dist[u] + 1
                    queue.append(v)
        return -1

    # Calculate shortest path for bus (roads) from 1 to n
    # Road exists between x and y if NO railway exists
    def bfs_road():
        if n == 1:
            return 0
        dist = [-1] * (n + 1)
        dist[1] = 0
        queue = [1]
        while queue:
            u = queue.pop(0)
            if u == n:
                return dist[u]
            # Iterate all possible towns
            for v in range(1, n + 1):
                if u == v:
                    continue
                # Check if road exists (no railway)
                if v not in railway_adj[u]:
                    if dist[v] == -1:
                        dist[v] = dist[u] + 1
                        queue.append(v)
        return -1

    train_time = bfs_rail()
    bus_time = bfs_road()

    if train_time == -1 or bus_time == -1:
        print(-1)
    else:
        print(max(train_time, bus_time))

if __name__ == "__main__":
    solve()