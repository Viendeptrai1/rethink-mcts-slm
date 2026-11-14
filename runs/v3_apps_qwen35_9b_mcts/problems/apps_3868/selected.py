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

    # Flights to Metropolis (arrival): f_i != 0, t_i == 0
    # Flights from Metropolis (departure): f_i == 0, t_i != 0
    
    # We need to group flights by day.
    # Since days can be up to 10^6, we can use a list of lists or a dictionary.
    # Given constraints, a list of size 10^6 + 2 is feasible.
    MAX_DAY = 1000005
    
    arrivals = [[] for _ in range(MAX_DAY)]
    departures = [[] for _ in range(MAX_DAY)]
    
    for _ in range(m):
        d = int(next(iterator))
        f = int(next(iterator))
        t = int(next(iterator))
        c = int(next(iterator))
        
        if t == 0:
            # Arrival flight
            arrivals[d].append((f, c))
        else:
            # Departure flight
            departures[d].append((t, c))
            
    # Precompute prefix minimums for arrivals
    # min_cost_arrival[i] = minimum cost to have ALL n jury members in Metropolis by day i
    # If not all members can arrive by day i, this should be infinity.
    
    # We need to track the minimum cost for each city and the count of cities covered.
    # However, since we process day by day, we can maintain:
    # - current_min_cost[city]: the cheapest flight to city 'city' seen so far
    # - count_covered: number of cities that have at least one flight
    # - total_cost: sum of current_min_cost for all covered cities
    
    INF = float('inf')
    city_min_cost = [INF] * (n + 1)
    count_covered = 0
    total_cost = 0
    
    min_cost_arrival = [INF] * MAX_DAY
    
    for day in range(1, MAX_DAY):
        # Process arrivals for this day
        for city, cost in arrivals[day]:
            if city_min_cost[city] == INF:
                # First time seeing a flight for this city
                count_covered += 1
                total_cost += cost
                city_min_cost[city] = cost
            else:
                # Found a cheaper flight for this city
                if cost < city_min_cost[city]:
                    total_cost -= city_min_cost[city]
                    total_cost += cost
                    city_min_cost[city] = cost
        
        # If all cities are covered, record the total cost for this day
        if count_covered == n:
            min_cost_arrival[day] = total_cost
            
    # Precompute suffix minimums for departures
    # min_cost_departure[i] = minimum cost to send ALL n jury members back from day i onwards
    # The work happens for k days. If they arrive by day 'd', they work [d+1, d+k].
    # They must leave on or after day d+k+1.
    # So we need the min cost to send everyone back starting from day 'd+k+1'.
    
    city_min_cost_dep = [INF] * (n + 1)
    count_covered_dep = 0
    total_cost_dep = 0
    
    min_cost_departure = [INF] * MAX_DAY
    
    # Iterate backwards from MAX_DAY - 1 down to 1
    for day in range(MAX_DAY - 1, 0, -1):
        # Process departures for this day
        for city, cost in departures[day]:
            if city_min_cost_dep[city] == INF:
                count_covered_dep += 1
                total_cost_dep += cost
                city_min_cost_dep[city] = cost
            else:
                if cost < city_min_cost_dep[city]:
                    total_cost_dep -= city_min_cost_dep[city]
                    total_cost_dep += cost
                    city_min_cost_dep[city] = cost
        
        if count_covered_dep == n:
            min_cost_departure[day] = total_cost_dep
            
    # Now find the minimum total cost
    # We need to choose a day 'd' such that:
    # 1. Everyone arrives by day 'd' (min_cost_arrival[d] is valid)
    # 2. Everyone leaves on or after day 'd + k + 1' (min_cost_departure[d + k + 1] is valid)
    # Note: The problem says "On his arrival day and departure day jury member is not able to discuss".
    # So if they arrive on day d, they are free starting day d+1.
    # They need k days of work: d+1, d+2, ..., d+k.
    # They must leave on day >= d+k+1.
    
    ans = INF
    
    # The latest possible arrival day is MAX_DAY - k - 2 (so that d+k+1 <= MAX_DAY-1 roughly)
    # Actually, we just iterate d where min_cost_arrival[d] is valid.
    # And check if d + k + 1 is within bounds and has a valid departure cost.
    
    for d in range(1, MAX_DAY):
        if min_cost_arrival[d] == INF:
            continue
        
        leave_day = d + k + 1
        if leave_day >= MAX_DAY:
            continue
            
        if min_cost_departure[leave_day] == INF:
            continue
            
        current_total = min_cost_arrival[d] + min_cost_departure[leave_day]
        if current_total < ans:
            ans = current_total
            
    if ans == INF:
        print("-1")
    else:
        print(ans)

if __name__ == '__main__':
    solve()