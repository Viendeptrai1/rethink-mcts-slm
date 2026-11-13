import sys
from collections import defaultdict, deque

def find_maximum_fee(N, P, X, Y, partnerships, M, swerc_banks):
    def can_achieve_cheapest_with_fee(max_fee):
        graph = defaultdict(list)
        for a, b, c in partnerships:
            if c <= max_fee:
                graph[a].append((b, c))
                graph[b].append((a, c))
        
        # BFS to find the shortest path from X to Y
        queue = deque([(X, 0)])
        visited = {X}
        
        while queue:
            current_bank, current_cost = queue.popleft()
            if current_bank == Y:
                return True
            for neighbor, fee in graph[current_bank]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, current_cost + fee))
        
        return False

    # Check if there is a path without any fee
    if can_achieve_cheapest_with_fee(0):
        return "Infinity"

    # Binary search for the maximum possible fee
    low, high = 1, 10**9
    result = "Impossible"
    
    while low <= high:
        mid = (low + high) // 2
        if can_achieve_cheapest_with_fee(mid):
            result = mid
            low = mid + 1
        else:
            high = mid - 1
    
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