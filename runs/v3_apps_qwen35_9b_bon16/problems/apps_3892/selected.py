import sys
from collections import defaultdict

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    n = int(next(iterator))
    m = int(next(iterator))
    
    # Store candies by their starting station
    # candies[start] = list of destinations
    candies = defaultdict(list)
    
    for _ in range(m):
        a = int(next(iterator))
        b = int(next(iterator))
        candies[a].append(b)
    
    # Precompute distances from any station u to any station v in a circular manner
    # distance(u, v) = (v - u) % n, but we want positive result
    def get_dist(u, v):
        if u == v:
            return 0
        if v > u:
            return v - u
        else:
            return n - (u - v)
    
    results = []
    
    # For each starting station 'start' (from 1 to n)
    for start in range(1, n + 1):
        total_time = 0
        
        # Group stations by how many candies originate there
        # We need to process each station that has candies
        # The strategy: 
        # 1. The train must visit each station 's' that has at least one candy exactly (count[s] - 1) times 
        #    after the first time it picks up a candy from 's', because it can only pick up one candy per visit.
        # 2. On the final visit to 's', it picks up the last candy and delivers it.
        # 
        # Actually, let's rethink the optimal strategy for a fixed start:
        # The train moves in a circle. At any station 's' with k candies, the train must stop at 's' exactly k times
        # to pick up all k candies. The first time it passes 's', it picks one. Then it continues around, picks another, etc.
        # The last candy from 's' will be delivered at some station 'dest'.
        # 
        # However, the train doesn't necessarily pick up candies from stations in order of distance.
        # But note: The train moves in a fixed circular direction. It cannot jump.
        # So the sequence of stations visited is start, start+1, ..., n, 1, ..., start-1, start, ...
        # 
        # For a station 's' with k candies:
        # - The train will visit 's' for the first time at some time T1.
        # - It picks one candy and leaves.
        # - Then it goes around the circle (taking n seconds) and comes back to 's' at T1 + n.
        # - It picks the second candy.
        # - ...
        # - It picks the k-th candy at T1 + (k-1)*n.
        # Then it travels to the destination of that last candy.
        # 
        # But wait, the train might not pick the last candy from 's' immediately upon returning? 
        # Actually, the constraint is "at most one candy can be loaded from a station ... before it leaves".
        # So yes, to get k candies from 's', the train must be at 's' k times.
        # The earliest times it can be at 's' are:
        #   First visit: when the train first reaches 's' from 'start'.
        #   Subsequent visits: every n seconds after that.
        # 
        # So for station 's' with k candies, the last candy is picked up at time:
        #   first_visit_time(s) + (k - 1) * n
        # Then the train must travel from 's' to the destination of that last candy.
        # Let the last candy from 's' be destined for 'd'. The travel time is get_dist(s, d).
        # So the time when the last candy from 's' is delivered is:
        #   first_visit_time(s) + (k - 1) * n + get_dist(s, d)
        # 
        # However, the train can choose WHICH candy to pick last from station 's'.
        # To minimize the total time, for each station 's', we should choose the candy with the destination 'd'
        # that minimizes (get_dist(s, d)).
        # Why? Because the pickup time is fixed for the last candy (first_visit + (k-1)*n), 
        # and we just add the travel time to the destination. So we pick the d that is closest to s.
        # 
        # But wait, is it possible that the train delivers a candy from 's' that was picked up earlier,
        # and that delivery happens later than the delivery of the last candy from 's'?
        # The delivery time of a candy picked up at time T from s to d is T + get_dist(s, d).
        # The last candy from 's' is picked up at T_last = T_first + (k-1)*n.
        # Its delivery time is T_last + min_dist(s, destinations).
        # Any earlier candy from 's' was picked up at T_first + (k-2)*n, etc.
        # Since get_dist is always non-negative, T_last + min_dist >= T_last >= T_earlier + get_dist?
        # Not necessarily. 
        # Example: T_first=0, n=100. k=2. 
        # Candy1: d1=1 (dist=1). Picked at 0, delivered at 1.
        # Candy2: d2=90 (dist=90). Picked at 100, delivered at 190.
        # Last delivery is 190.
        # If we swap? 
        # Candy1: d1=90. Picked at 0, delivered at 90.
        # Candy2: d2=1. Picked at 100, delivered at 101.
        # Last delivery is 101.
        # So we should indeed pick the candy with the smallest destination distance to be the last one?
        # Wait, if we pick the one with small distance first, then the one with large distance second:
        #   Pick small at 0 -> deliver at 1.
        #   Pick large at 100 -> deliver at 100+large_dist.
        #   Max = 100+large_dist.
        # If we pick large first, small second:
        #   Pick large at 0 -> deliver at 0+large_dist.
        #   Pick small at 100 -> deliver at 100+small_dist.
        #   Max = max(large_dist, 100+small_dist).
        # Since large_dist >= 1 and small_dist >= 1, and typically large_dist could be large.
        # But note: 100 + small_dist might be larger than large_dist? 
        # Example: small_dist=1, large_dist=50. 
        # Strategy 1 (small first): max(1, 100+50) = 150.
        # Strategy 2 (large first): max(50, 100+1) = 101.
        # So Strategy 2 is better.
        # Conclusion: For a station with k candies, we should leave the candy with the SMALLEST destination distance 
        # for LAST. Because the penalty of waiting (k-1)*n is fixed, but the travel time added is minimized if we pick the closest destination last.
        # 
        # Therefore, for each station 's' with candies:
        #   k = count of candies at s
        #   Calculate min_dist = min(get_dist(s, d) for all d in destinations of s)
        #   The delivery time for the last candy from s is: first_visit_time(s) + (k-1)*n + min_dist
        # 
        # The total time required for the entire task starting at 'start' is the maximum over all stations 's' (that have candies)
        # of (first_visit_time(s) + (k-1)*n + min_dist(s)).
        # Note: If a station has no candies, we ignore it.
        # Also, if there are no candies at all (m=0), time is 0. But m>=1.
        
        max_time = 0
        
        # Calculate first_visit_time(s) for each station s from 1 to n
        # The train starts at 'start'. 
        # Time to reach s: 
        #   if s >= start: dist = s - start
        #   else: dist = (n - start) + s
        #   Actually: (s - start) % n
        first_visit_times = {}
        for s in range(1, n + 1):
            if s >= start:
                dist = s - start
            else:
                dist = n - start + s
            first_visit_times[s] = dist
        
        # For each station that has candies
        for s, destinations in candies.items():
            k = len(destinations)
            if k == 0:
                continue
            
            # Find the minimum distance from s to any destination
            min_d = float('inf')
            for d in destinations:
                d_val = get_dist(s, d)
                if d_val < min_d:
                    min_d = d_val
            
            # Time when the last candy from s is delivered
            current_time = first_visit_times[s] + (k - 1) * n + min_d
            if current_time > max_time:
                max_time = current_time
        
        results.append(max_time)
    
    # Print results
    print(*(results))

if __name__ == "__main__":
    solve()