import sys
from collections import defaultdict
import heapq

def largest_fee(N, P, X, Y, partnerships, M, swerc_banks):
    def dijkstra(start, fee_limit):
        distances = {bank: float('inf') for bank in range(1, N+1)}
        distances[start] = 0
        priority_queue = [(0, start)]
        
        while priority_queue:
            current_distance, current_bank = heapq.heappop(priority_queue)
            
            if current_distance > distances[current_bank]:
                continue
            
            for neighbor, fee in graph[current_bank]:
                if neighbor in swerc_banks and fee > fee_limit:
                    continue
                
                distance = current_distance + fee
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(priority_queue, (distance, neighbor))
        
        return distances[Y]
    
    graph = defaultdict(list)
    for a, b, c in partnerships:
        graph[a].append((b, c))
        graph[b].append((a, c))
    
    swerc_banks_set = set(swerc_banks)
    
    if Y not in swerc_banks_set:
        return "Infinity"
    
    low, high = 0, 10**9
    answer = -1
    
    while low <= high:
        mid = (low + high) // 2
        if dijkstra(X, mid) < float('inf'):
            answer = mid
            low = mid + 1
        else:
            high = mid - 1
    
    return answer if answer != -1 else "Impossible"

def main():
    input = sys.stdin.read
    data = input().split()
    
    idx = 0
    N = int(data[idx])
    P = int(data[idx + 1])
    X = int(data[idx + 2])
    Y = int(data[idx + 3])
    idx += 4
    
    partnerships = []
    for _ in range(P):
        a = int(data[idx])
        b = int(data[idx + 1])
        c = int(data[idx + 2])
        partnerships.append((a, b, c))
        idx += 3
    
    M = int(data[idx])
    idx += 1
    
    swerc_banks = []
    for _ in range(M):
        bank_id = int(data[idx])
        swerc_banks.append(bank_id)
        idx += 1
    
    result = largest_fee(N, P, X, Y, partnerships, M, swerc_banks)
    print(result)

if __name__ == "__main__":
    main()