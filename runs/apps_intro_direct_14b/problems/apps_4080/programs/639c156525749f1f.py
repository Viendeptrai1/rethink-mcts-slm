import sys
from collections import defaultdict

def main():
    import sys
    import heapq
    
    def read_ints():
        return list(map(int, sys.stdin.readline().split()))
    
    n, m = read_ints()
    a = read_ints()
    
    segments = []
    for _ in range(m):
        l, r = read_ints()
        segments.append((l-1, r-1))
    
    # Create a graph where each node is an index in the array
    graph = defaultdict(list)
    for i in range(n):
        graph[i].append((i, 0))  # Stay at the same position with no cost
    
    # Add edges for each segment
    for j, (l, r) in enumerate(segments):
        graph[l].append((r, 1))  # Move from l to r with cost 1
        graph[r].append((l, 1))  # Move from r to l with cost 1
    
    # Dijkstra's algorithm to find the minimum cost to reach each position
    min_cost = [float('inf')] * n
    pq = [(0, 0)]  # (cost, position)
    while pq:
        cost, pos = heapq.heappop(pq)
        if cost > min_cost[pos]:
            continue
        for next_pos, next_cost in graph[pos]:
            new_cost = cost + next_cost
            if new_cost < min_cost[next_pos]:
                min_cost[next_pos] = new_cost
                heapq.heappush(pq, (new_cost, next_pos))
    
    # Calculate the maximum difference after applying the segments
    max_diff = 0
    best_segments = []
    for j, (l, r) in enumerate(segments):
        new_a = a[:]
        for i in range(l, r+1):
            new_a[i] -= 1
        diff = max(new_a) - min(new_a)
        if diff > max_diff:
            max_diff = diff
            best_segments = [j+1]
        elif diff == max_diff:
            best_segments.append(j+1)
    
    # Output the result
    print(max_diff)
    print(len(best_segments))
    print(*best_segments)

if __name__ == "__main__":
    main()