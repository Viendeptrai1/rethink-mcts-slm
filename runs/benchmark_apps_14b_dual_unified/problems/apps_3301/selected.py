import sys
import heapq

def dijkstra(graph, start, end):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    priority_queue = [(0, start)]
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        if current_distance > distances[current_node]:
            continue
        
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))
    
    return distances[end]

def find_largest_fee(N, P, X, Y, partnerships, M, swerc_banks):
    graph = {i: {} for i in range(1, N + 1)}
    
    for a, b, c in partnerships:
        graph[a][b] = c
        graph[b][a] = c
    
    min_fee_without_extra = dijkstra(graph, X, Y)
    
    if min_fee_without_extra == float('inf'):
        return "Impossible"
    
    swerc_graph = {i: {} for i in swerc_banks}
    
    for a, b, c in partnerships:
        if a in swerc_banks and b in swerc_banks:
            swerc_graph[a][b] = c
            swerc_graph[b][a] = c
    
    max_extra_fee = 0
    
    for a in swerc_banks:
        for b in swerc_banks:
            if a != b:
                for c in swerc_banks:
                    if c != a and c != b:
                        if a in swerc_graph and b in swerc_graph and c in swerc_graph:
                            if a in swerc_graph[c] and b in swerc_graph[c]:
                                max_extra_fee = max(max_extra_fee, swerc_graph[a][c] + swerc_graph[c][b] - swerc_graph[a][b])
    
    if max_extra_fee == 0:
        return "Infinity"
    
    return max_extra_fee

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
    
    swerc_banks = set(map(int, data[index:index + M]))
    index += M
    
    result = find_largest_fee(N, P, X, Y, partnerships, M, swerc_banks)
    print(result)

if __name__ == "__main__":
    main()