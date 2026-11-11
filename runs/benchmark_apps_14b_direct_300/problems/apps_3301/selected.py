import sys
import heapq

def dijkstra(graph, start, end, max_fee):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    priority_queue = [(0, start)]
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        if current_distance > distances[current_node]:
            continue
        
        for neighbor, weight in graph[current_node].items():
            if weight <= max_fee:
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
    
    def can_transfer_with_fee(max_fee):
        return dijkstra(graph, X, Y, max_fee) != float('inf')
    
    low, high = 0, 1000000000
    result = "Impossible"
    
    while low <= high:
        mid = (low + high) // 2
        if can_transfer_with_fee(mid):
            result = mid
            low = mid + 1
        else:
            high = mid - 1
    
    if result == "Impossible" and can_transfer_with_fee(float('inf')):
        result = "Infinity"
    
    return result

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