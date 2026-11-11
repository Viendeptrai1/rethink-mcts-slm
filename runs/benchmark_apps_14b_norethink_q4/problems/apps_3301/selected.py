import sys
import heapq

def dijkstra(graph, start, end, swerc_banks):
    dist = {node: float('inf') for node in graph}
    dist[start] = 0
    priority_queue = [(0, start)]
    
    while priority_queue:
        current_dist, current_node = heapq.heappop(priority_queue)
        
        if current_node == end:
            return current_dist
        
        for neighbor, weight in graph[current_node].items():
            if neighbor in swerc_banks:
                distance = current_dist + weight
                if distance < dist[neighbor]:
                    dist[neighbor] = distance
                    heapq.heappush(priority_queue, (distance, neighbor))
    
    return float('inf')

def find_largest_fee(N, P, X, Y, partnerships, M, swerc_banks):
    graph = {i: {} for i in range(1, N + 1)}
    
    for a, b, c in partnerships:
        graph[a][b] = c
        graph[b][a] = c
    
    baseline_cost = dijkstra(graph, X, Y, set(range(1, N + 1)))
    
    if baseline_cost == float('inf'):
        return "Impossible"
    
    max_fee = max(c for _, _, c in partnerships)
    min_fee = 1
    
    while min_fee <= max_fee:
        mid_fee = (min_fee + max_fee) // 2
        modified_graph = {i: {} for i in range(1, N + 1)}
        
        for a, b, c in partnerships:
            if c + mid_fee < baseline_cost:
                modified_graph[a][b] = c + mid_fee
                modified_graph[b][a] = c + mid_fee
        
        swerc_cost = dijkstra(modified_graph, X, Y, swerc_banks)
        
        if swerc_cost < baseline_cost:
            min_fee = mid_fee + 1
        else:
            max_fee = mid_fee - 1
    
    if min_fee - 1 > 0:
        return min_fee - 1
    else:
        return "Infinity"

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    N = int(data[index])
    P = int(data[index + 1])
    X = int(data[index + 2])
    Y = int(data[index + 3])
    index += 4
    
    partnerships = []
    for _ in range(P):
        a = int(data[index])
        b = int(data[index + 1])
        c = int(data[index + 2])
        partnerships.append((a, b, c))
        index += 3
    
    M = int(data[index])
    index += 1
    swerc_banks = set(int(data[index + i]) for i in range(M))
    index += M
    
    result = find_largest_fee(N, P, X, Y, partnerships, M, swerc_banks)
    print(result)

if __name__ == "__main__":
    main()