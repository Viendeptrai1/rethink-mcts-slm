import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    iterator = iter(data)
    
    try:
        n = int(next(iterator))
        m = int(next(iterator))
        k = int(next(iterator))
    except StopIteration:
        return

    # Flights to Metropolis (arrive at 0): f != 0, t == 0
    # Flights from Metropolis (depart to f): f == 0, t != 0
    
    # We need to find a window of days [start_day, end_day] such that:
    # - All jury members (1..n) can arrive on or before start_day - 1 (so they are present on start_day)
    # - All jury members stay until end_day + 1 (so they are present on end_day)
    # Actually, the problem states:
    # "On his arrival day and departure day jury member is not able to discuss the olympiad."
    # They need to work for k days.
    # If they arrive on day A, they can work starting from A+1.
    # If they leave on day B, they can work until B-1.
    # So the working interval for a person arriving on A and leaving on B is [A+1, B-1].
    # We need an interval of length k: (B-1) - (A+1) + 1 >= k  => B - A - 1 >= k => B - A >= k + 1.
    # Let the working days be [W, W+k-1].
    # Then arrival day A <= W-1, and departure day B >= W+k.
    # So for a fixed start of work W, everyone must arrive by W-1 and leave by W+k.
    
    # Max day is 10^6. Let's collect flights by day.
    # We will process days from 1 to max_day.
    
    max_day = 1000000
    # To optimize, we can find the actual max day present in input to limit loops, 
    # but 10^6 is small enough for O(max_day) if operations inside are O(1).
    # However, sorting flights by day is safer and often faster if m is small compared to max_day.
    
    # Group flights by day
    # flights_to[day] = list of (from_city, cost)
    # flights_from[day] = list of (to_city, cost)
    
    # Since we need to check "can everyone arrive by day X", we can maintain the minimum cost for each city to arrive by day X.
    # Similarly for departure.
    
    # Let's store events.
    # Actually, we can just sort all flights by day.
    
    flights_to = [] # (day, from_city, cost)
    flights_from = [] # (day, to_city, cost)
    
    max_d_in = -1
    max_d_out = -1
    
    for _ in range(m):
        d = int(next(iterator))
        f = int(next(iterator))
        t = int(next(iterator))
        c = int(next(iterator))
        
        if t == 0:
            # To Metropolis
            flights_to.append((d, f, c))
            if d > max_d_in: max_d_in = d
        else:
            # From Metropolis
            flights_from.append((d, t, c))
            if d > max_d_out: max_d_out = d
            
    # Sort flights by day
    flights_to.sort(key=lambda x: x[0])
    flights_from.sort(key=lambda x: x[0])
    
    # Precompute prefix minimums for "arrival by day D"
    # arrive_min[d][city] = min cost to bring city to Metropolis on or before day d
    # But storing a full 2D array is too big if we iterate day by day and update all cities?
    # Wait, we only care about the day when a new flight arrives.
    # We can compress days or just iterate through the sorted unique days of flights.
    
    # Strategy:
    # 1. Identify all unique days where any flight occurs (both to and from).
    # 2. Create an array `min_cost_arrive` of size (max_day + 2) where min_cost_arrive[d] is a bitmask or count of satisfied cities?
    # No, n is up to 10^5. We cannot maintain a full state per day for all cities.
    # However, we only need to know: "Is every city covered?" and "What is the sum of costs?".
    # Since each city only needs one ticket, once a city is covered by a cheaper flight earlier, we keep that.
    # If a new flight appears for a city that wasn't covered yet, we add its cost and increment covered count.
    # If it's covered, we update if cheaper.
    
    # We can simulate day by day from 1 to max_possible_day (10^6).
    # We maintain:
    # - `current_cost_arrive`: total cost of cheapest tickets for all covered cities so far.
    # - `count_covered_arrive`: number of cities covered.
    # - `min_cost_arrive_day[d]`: the minimum `current_cost_arrive` achievable such that all n cities are covered by day d.
    # If not all covered, we can mark it as infinity.
    # But wait, the cost might decrease later? No, if we fix the deadline "by day D", we take the cheapest flights <= D.
    # As D increases, the set of available flights grows, so costs can only decrease (or stay same).
    # So `min_cost_arrive_day[d]` is non-increasing with d.
    # Actually, we want `min_cost_arrive_day[d]` to be the total cost using the best flights up to day d for ALL cities.
    # If at day d, not all cities are covered, then `min_cost_arrive_day[d] = infinity`.
    
    # Similarly for departure: `min_cost_depart_day[d]` = min cost to send everyone back on or after day d.
    # As d increases, fewer flights are available (only those >= d), so cost increases.
    # We can precompute this by iterating backwards from max_day down to 1.
    
    # Algorithm:
    # 1. Iterate d from 1 to 1000000. Update arrival costs. Store `best_arrive[d]`.
    #    If all cities covered, `best_arrive[d]` = current total cost. Else infinity.
    # 2. Iterate d from 1000000 down to 1. Update departure costs. Store `best_depart[d]`.
    #    If all cities covered, `best_depart[d]` = current total cost. Else infinity.
    #    Note: Departure flights are on day d or later. So when at day d, we consider flights with day >= d.
    #    Backwards iteration: at step d, add flights with day == d to our pool.
    
    # Complexity:
    # Days: 10^6.
    # Flights: 10^5.
    # Updating costs: When a new flight arrives for a city not yet covered, cost += c, count++.
    # When a city already covered, cost = min(old, new).
    # We need to store the current best cost for each city to compare.
    # `best_city_cost_arrive` array of size n+1.
    # `best_city_cost_depart` array of size n+1.
    # `count_arrive`, `count_depart`.
    
    # Let's implement.
    
    LIMIT = 1000000
    INF = float('inf')
    
    # Initialize
    best_city_cost_arrive = [INF] * (n + 1)
    count_arrive = 0
    current_total_arrive = 0
    best_arrive = [INF] * (LIMIT + 2)
    
    # Sort flights_to by day
    flights_to.sort(key=lambda x: x[0])
    ptr = 0
    num_flights_to = len(flights_to)
    
    for d in range(1, LIMIT + 1):
        # Process all flights arriving on day d
        while ptr < num_flights_to and flights_to[ptr][0] == d:
            _, city, cost = flights_to[ptr]
            ptr += 1
            if best_city_cost_arrive[city] == INF:
                # First time this city is covered
                count_arrive += 1
                current_total_arrive += cost
                best_city_cost_arrive[city] = cost
            else:
                if cost < best_city_cost_arrive[city]:
                    current_total_arrive -= best_city_cost_arrive[city]
                    current_total_arrive += cost
                    best_city_cost_arrive[city] = cost
        
        if count_arrive == n:
            best_arrive[d] = current_total_arrive
        else:
            best_arrive[d] = INF
            
    # Now for departure
    best_city_cost_depart = [INF] * (n + 1)
    count_depart = 0
    current_total_depart = 0
    best_depart = [INF] * (LIMIT + 2)
    
    # Sort flights_from by day
    flights_from.sort(key=lambda x: x[0])
    # We need to process backwards. Let's reverse the list or use index.
    # Better: sort ascending, then iterate from end.
    ptr_from = len(flights_from) - 1
    num_flights_from = len(flights_from)
    
    for d in range(LIMIT, 0, -1):
        # Process all flights departing on day d
        while ptr_from >= 0 and flights_from[ptr_from][0] == d:
            _, city, cost = flights_from[ptr_from]
            ptr_from -= 1
            if best_city_cost_depart[city] == INF:
                count_depart += 1
                current_total_depart += cost
                best_city_cost_depart[city] = cost
            else:
                if cost < best_city_cost_depart[city]:
                    current_total_depart -= best_city_cost_depart[city]
                    current_total_depart += cost
                    best_city_cost_depart[city] = cost
        
        if count_depart == n:
            best_depart[d] = current_total_depart
        else:
            best_depart[d] = INF
            
    # Now find min total cost for a valid window
    # Work period: [W, W+k-1]
    # Arrival must be by W-1. Departure must be from W+k.
    # So we need to sum best_arrive[W-1] and best_depart[W+k].
    # W ranges such that W-1 >= 1 (so W>=2) and W+k <= LIMIT.
    # Actually, arrival flights can be on day 1. So W-1 >= 1 => W >= 2.
    # Departure flights can be on day LIMIT. So W+k <= LIMIT.
    # Also, we need to ensure W-1 is a valid day index in our array.
    # Our array goes up to LIMIT.
    
    min_total = INF
    
    # W is the first day of work.
    # Arrival deadline: W-1.
    # Departure start: W+k.
    # Constraints on W:
    # 1 <= W-1 <= LIMIT  => 2 <= W <= LIMIT+1
    # W+k <= LIMIT       => W <= LIMIT - k
    # So W in [2, LIMIT - k]
    
    # However, we must check if best_arrive[W-1] and best_depart[W+k] are both valid (not INF).
    
    start_W = 2
    end_W = LIMIT - k
    
    if end_W < start_W:
        print("-1")
        return

    for W in range(start_W, end_W + 1):
        arrive_day = W - 1
        depart_day = W + k
        
        if arrive_day > LIMIT or depart_day > LIMIT:
            continue
            
        cost = best_arrive[arrive_day] + best_depart[depart_day]
        if cost < min_total:
            min_total = cost
            
    if min_total == INF:
        print("-1")
    else:
        print(min_total)

if __name__ == '__main__':
    solve()