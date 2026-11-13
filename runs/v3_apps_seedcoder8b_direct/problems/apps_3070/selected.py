import sys
import heapq
from collections import defaultdict, deque

def earliest_booking_time():
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    M = int(data[1])
    
    index = 2
    trains = []
    
    for _ in range(M):
        X = int(data[index])
        S = int(data[index + 1])
        T = int(data[index + 2])
        L = int(data[index + 3])
        index += 4
        trains.append((X, S, T, L))
    
    # Graph to store the earliest arrival times at each station
    graph = defaultdict(list)
    
    # Build the graph
    for X, S, T, L in trains:
        # Calculate the actual departure and arrival times
        actual_departure = S + L
        actual_arrival = T + L
        # Add the edge from station X to X+1
        graph[X].append((X + 1, actual_departure, actual_arrival))
    
    # Priority queue for Dijkstra's algorithm
    pq = []
    # Earliest arrival times at each station
    earliest_arrival = [float('inf')] * (N + 1)
    earliest_arrival[1] = 0
    heapq.heappush(pq, (0, 1))  # (arrival_time, station)
    
    while pq:
        current_time, current_station = heapq.heappop(pq)
        
        if current_station == N:
            # If we reach station N, check if the journey is possible
            if current_time >= 1800:
                print(current_time)
                return
        
        for next_station, departure_time, arrival_time in graph[current_station]:
            if arrival_time < earliest_arrival[next_station]:
                earliest_arrival[next_station] = arrival_time
                heapq.heappush(pq, (arrival_time, next_station))
    
    # If we finish the loop without reaching station N in 1800 seconds or more
    print("impossible")