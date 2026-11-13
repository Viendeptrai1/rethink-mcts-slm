import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    iterator = iter(data)
    n = int(next(iterator))
    m = int(next(iterator))
    
    # Group candies by starting station
    # stations[i] will be a list of distances to deliver candies starting at station i+1
    stations = [[] for _ in range(n + 1)]
    
    for _ in range(m):
        a = int(next(iterator))
        b = int(next(iterator))
        # Distance from a to b in a circular manner
        dist = (b - a) % n
        if dist == 0:
            dist = n
        stations[a].append(dist)
    
    results = []
    
    for start in range(1, n + 1):
        # Calculate time if train starts at 'start'
        # The train must visit each station that has candies at least once.
        # For a station with k candies, the train will visit it k times.
        # The last candy picked up at station 's' will be delivered after:
        # (time to reach 's' from 'start' + time to deliver the last candy from 's')
        # The time to deliver the last candy from 's' is:
        # (time to reach 's' from 'start' + (n - 1) + max_dist_at_s)
        # Wait, let's re-derive carefully.
        
        # Strategy:
        # The train moves in a circle. It picks up one candy per visit to a station with candies.
        # If a station has k candies, the train must visit it k times.
        # The last time it visits a station 's' (with k candies), it picks up the last candy.
        # Then it travels to the destination of that last candy.
        # The total time is determined by the "bottleneck" station: the one that forces the train to go the furthest.
        # Specifically, for each station 's' that has candies:
        # 1. The train visits 's' for the first time, picks up one candy, delivers it.
        # 2. It continues visiting other stations...
        # 3. Eventually, it returns to 's' for the second time (if k=2), picks up another, etc.
        # 4. The last candy at 's' is picked up on the k-th visit.
        # 5. After picking up the last candy at 's', the train travels to its destination.
        #
        # Let's calculate the completion time for each station 's' independently.
        # The train starts at 'start'.
        # Distance from 'start' to 's' (first visit): d_start_s = (s - start) % n; if 0 then n.
        # Actually, simpler: distance = (s - start) % n. If 0, it means start==s, so distance is 0?
        # No, if start == s, the train is already there. It can pick up immediately.
        # But the problem says "travel to its next station".
        # If start == s, the train is at s at time 0. It can load.
        # So distance to first visit is 0 if start == s, else (s - start) % n.
        # However, the standard formula (s - start) % n gives 0 if s==start.
        # Let's define dist(u, v) as steps from u to v.
        # dist(u, v) = (v - u) % n. If result is 0, it means u==v, so 0 steps.
        # But wait, if u==v, do we need to move? No.
        # So dist(u, v) = (v - u) % n.
        
        # For a station 's' with candies:
        # Let k = number of candies at 's'.
        # Let max_d = maximum distance among candies at 's' (distance from s to destination).
        # The train visits 's' for the first time at time T1 = (s - start) % n.
        # It picks up one candy.
        # It visits 's' again at T1 + n, picks up second.
        # ...
        # It visits 's' for the k-th time at T1 + (k-1)*n.
        # At this moment, it picks up the last candy.
        # Then it travels to the destination of this last candy.
        # The time taken from picking up to delivering is max_d.
        # So the completion time for station 's' is: T1 + (k-1)*n + max_d.
        # Note: If k=0, this station doesn't contribute.
        
        # The total time required is the maximum of these completion times over all stations 's' that have candies.
        # If no candies, time is 0.
        
        max_time = 0
        
        for s in range(1, n + 1):
            if not stations[s]:
                continue
            
            k = len(stations[s])
            # Calculate distance from start to s
            d_start_s = (s - start) % n
            
            # Find max distance for candies at s
            max_d = 0
            for d in stations[s]:
                if d > max_d:
                    max_d = d
            
            # Time to finish all candies at station s
            # First visit at d_start_s
            # (k-1) full circles later
            # Then travel max_d
            time_s = d_start_s + (k - 1) * n + max_d
            
            if time_s > max_time:
                max_time = time_s
        
        results.append(max_time)
    
    print(*(results))

if __name__ == '__main__':
    solve()