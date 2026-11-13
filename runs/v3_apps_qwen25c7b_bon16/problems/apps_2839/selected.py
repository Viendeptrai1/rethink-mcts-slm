import sys
import heapq

def dijkstra(V, adj_list, start):
    dist = [float('inf')] * V
    dist[start] = 0
    pq = [(0, start)]
    while pq:
        current_dist, current_node = heapq.heappop(pq)
        if current_dist > dist[current_node]:
            continue
        for neighbor, weight in adj_list[current_node]:
            distance = current_dist + weight
            if distance < dist[neighbor]:
                dist[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
    return dist

def count_paths(V, adj_list, s, t):
    dist_s_to_t = dijkstra(V, adj_list, s)
    if dist_s_to_t[t] == float('inf'):
        return 0
    
    def dfs(node, target, visited_edges, path_cost):
        if node == target:
            if path_cost == dist_s_to_t[target]:
                return 1
            return 0
        count = 0
        for neighbor, weight in adj_list[node]:
            if (node, neighbor, weight) not in visited_edges and (neighbor, node, weight) not in visited_edges:
                visited_edges.add((node, neighbor, weight))
                count += dfs(neighbor, target, visited_edges, path_cost + weight)
                visited_edges.remove((node, neighbor, weight))
        return count
    
    return dfs(s, t, set(), 0)

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    V = int(data[index])
    index += 1
    E = int(data[index])
    index += 1
    
    adj_list = [[] for _ in range(V)]
    for i in range(E):
        u = int(data[index])
        index += 1
        v = int(data[index])
        index += 1
        w = int(data[index])
        index += 1
        adj_list[u].append((v, w))
    
    s = int(data[index])
    index += 1
    t = int(data[index])
    index += 1
    
    result = count_paths(V, adj_list, s, t)
    print(result)