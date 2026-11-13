import sys
import heapq
from collections import defaultdict, deque

def find_earliest_start_time():
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    N = int(data[index])
    M = int(data[index + 1])
    index += 2
    
    graph = defaultdict(list)
    
    for _ in range(M):
        X = int(data[index]) - 1  # Convert to 0-based index
        S = int(data[index + 1])
        T = int(data[index + 2])
        L = int(data[index + 3])
        index += 4
        
        graph[X].append((S, T, L))
    
    def is_reachable_under_30_minutes():
        # Early start time set to 0
        min_start_time = 0
        # Priority queue to determine the earliest time to reach each station
        pq = [(0, 0)]  # (arrival time, station)
        
        while pq:
            current_arrival, station = heapq.heappop(pq)
            
            if station == N - 1 and current_arrival >= 1800:
                return True
            
            for next_station, (S, T, L) in enumerate(graph[station], start=station + 1):
                next_arrival = max(S + L, current_arrival)
                
                # If the next station can be reached before T + L, consider it
                if next_arrival <= T + L:
                    heapq.heappush(pq, (next_arrival, next_station))
        
        return False
    
    if is_reachable_under_30_minutes():
        print(1800)
    else:
        print("impossible")

find_earliest_start_time()