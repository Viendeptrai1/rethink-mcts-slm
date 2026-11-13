import sys
from collections import defaultdict, deque
import heapq

def find_maximum_fee(N, P, X, Y, partnerships, M, swerc_banks):
    # Create adjacency list for the graph
    graph = defaultdict(list)
    for a, b, c in partnerships:
        graph[a].append((b, c))
        graph[b].append((a, c))
    
    # Function to check if there's a path with max fee less than or equal to `max_fee`
    def can_transfer_with_max_fee(max_fee):
        # Use Dijkstra's algorithm to find the shortest path with constraints
        pq = [(0, X)]  # (current cost, current bank)
        visited = set()
        
        while pq:
            current_cost, current_bank = heapq.heappop(pq)
            
            if current_bank in visited:
                continue
            visited.add(current_bank)
            
            if current_bank == Y:
                return True
            
            for neighbor, fee in graph[current_bank]:
                if neighbor not in visited and fee <= max_fee:
                    heapq.heappush(pq, (current_cost + fee, neighbor))
        
        return False
    
    # Binary search to find the maximum fee
    left, right = 0, 10**9
    result = "Impossible"
    
    while left <= right:
        mid = (left + right) // 2
        if can_transfer_with_max_fee(mid):
            result = mid
            left = mid + 1
        else:
            right = mid - 1
    
    # Check if the result is feasible
    if result == "Impossible":
        return "Impossible"
    
    # Check if the fee can be infinitely large
    if result == 10**9:
        return "Infinity"
    
    return result

def main():
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    N = int(data[index])
    index += 1
    P = int(data[index])
    index += 1
    X = int(data[index])
    index += 1
    Y = int(data[index])
    index += 1
    
    partnerships = []
    for _ in range(P):
        a = int(data[index])
        index += 1
        b = int(data[index])
        index += 1
        c = int(data[index])
        index += 1
        partnerships.append((a, b, c))
    
    M = int(data[index])
    index += 1
    swerc_banks = list(map(int, data[index:]))
    
    result = find_maximum_fee(N, P, X, Y, partnerships, M, swerc_banks)
    print(result)

if __name__ == "__main__":
    main()