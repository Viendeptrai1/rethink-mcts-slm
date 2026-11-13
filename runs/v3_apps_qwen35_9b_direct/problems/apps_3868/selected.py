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

    # Flights to Metropolis (f_i != 0, t_i == 0)
    # Flights from Metropolis (f_i == 0, t_i != 0)
    
    # We need to find a window [start_day, end_day] such that:
    # 1. All jury members can arrive in Metropolis on or before start_day.
    #    Actually, they must arrive on day <= start_day - 1? 
    #    Let's re-read: "On his arrival day and departure day jury member is not able to discuss".
    #    They need to work for k days.
    #    If they arrive on day A, they can start working on day A+1.
    #    They need to work on days A+1, ..., A+k.
    #    They must depart on day D >= A+k+1.
    #    So the working period is [A+1, A+k].
    #    The condition is: for every city i (1..n), there is an arrival flight <= A and a departure flight >= A+k+1.
    #    Wait, the problem says "gather everybody for k days".
    #    If they arrive on day d_arr, they are busy on d_arr. They can work starting d_arr+1.
    #    They need k days of work. So they work on d_arr+1, ..., d_arr+k.
    #    They must leave on day d_dep >= d_arr+k+1.
    #    So we need to choose a "start working day" S.
    #    Then everyone must arrive by day S-1.
    #    And everyone must depart on day >= S+k.
    #    Let's verify with the example.
    #    Example 1: n=2, m=6, k=5.
    #    Flights:
    #    1: 1->0 cost 5000 (arrives day 1)
    #    2: 2->0 cost 5500 (arrives day 3)
    #    3: 2->0 cost 6000 (arrives day 2)
    #    4: 0->2 cost 9000 (departs day 15)
    #    5: 0->1 cost 7000 (departs day 9)
    #    6: 0->2 cost 6500 (departs day 8)
    #    
    #    Note says: use flights on days 1, 2, 8, 9.
    #    Arrivals: City 1 on day 1. City 2 on day 2 (cheaper than day 3).
    #    Departures: City 1 on day 9. City 2 on day 8.
    #    If City 1 arrives day 1, works day 2..6 (5 days). Departs day 9 (>= 1+5+1=7). OK.
    #    If City 2 arrives day 2, works day 3..7 (5 days). Departs day 8 (>= 2+5+1=8). OK.
    #    So the "working period" is effectively determined by the latest arrival day among all members.
    #    Let L = max(arrival_day for all members).
    #    Then everyone must have arrived by day L.
    #    The work starts on day L+1 and ends on day L+k.
    #    Everyone must depart on day >= L+k+1.
    #    So we need to find a day L such that:
    #    1. It is possible for everyone to arrive by day L.
    #    2. It is possible for everyone to depart on day >= L+k+1.
    #    And we minimize (cost to arrive by L) + (cost to depart >= L+k+1).
    
    # Precompute min cost to bring everyone to Metropolis by day D for all D.
    # Let min_arrive_cost[D] = minimum total cost to have all n members in Metropolis by day D.
    # If not possible, infinity.
    
    # Similarly, min_depart_cost[D] = minimum total cost to send all n members back from Metropolis on day >= D.
    
    # Max day is 10^6.
    MAX_DAY = 1000005
    
    # Read flights
    # Store incoming flights: day -> list of (city, cost)
    # Store outgoing flights: day -> list of (city, cost)
    
    incoming = [[] for _ in range(MAX_DAY)]
    outgoing = [[] for _ in range(MAX_DAY)]
    
    for _ in range(m):
        d = int(next(iterator))
        f = int(next(iterator))
        t = int(next(iterator))
        c = int(next(iterator))
        
        if t == 0: # To Metropolis
            incoming[d].append((f, c))
        else: # From Metropolis
            outgoing[d].append((t, c))
            
    # Compute min_arrive_cost
    # We need the min cost to cover all cities 1..n.
    # We can maintain the current min cost for each city and a count of how many cities are covered.
    # Since we iterate day by day, we can update the costs.
    
    current_city_min_cost = [-1] * (n + 1)
    covered_count = 0
    total_arrive_cost = 0
    
    # To optimize, we can store the best cost seen so far for each city.
    # But we need the sum of best costs for all cities.
    # When a new flight comes for city c with cost c_val:
    #   if current_city_min_cost[c] == -1:
    #       current_city_min_cost[c] = c_val
    #       covered_count += 1
    #       total_arrive_cost += c_val
    #   else:
    #       if c_val < current_city_min_cost[c]:
    #           total_arrive_cost -= current_city_min_cost[c]
    #           current_city_min_cost[c] = c_val
    #           total_arrive_cost += c_val
    
    # We need an array for the result of min_arrive_cost for each day.
    min_arrive_cost = [float('inf')] * MAX_DAY
    
    # Iterate days
    for d in range(1, MAX_DAY):
        # Process incoming flights for day d
        for city, cost in incoming[d]:
            if current_city_min_cost[city] == -1:
                current_city_min_cost[city] = cost
                covered_count += 1
                total_arrive_cost += cost
            else:
                if cost < current_city_min_cost[city]:
                    total_arrive_cost -= current_city_min_cost[city]
                    current_city_min_cost[city] = cost
                    total_arrive_cost += cost
        
        if covered_count == n:
            min_arrive_cost[d] = total_arrive_cost
            
    # Now compute min_depart_cost
    # min_depart_cost[D] = min cost to send everyone back on day >= D.
    # This is equivalent to: for each day D, consider all flights from D to MAX_DAY.
    # We can iterate backwards from MAX_DAY-1 down to 1.
    # Maintain current min cost for each city and total cost.
    
    current_city_min_cost_out = [-1] * (n + 1)
    covered_count_out = 0
    total_depart_cost = 0
    
    min_depart_cost = [float('inf')] * MAX_DAY
    
    for d in range(MAX_DAY - 1, 0, -1):
        # Process outgoing flights for day d
        for city, cost in outgoing[d]:
            if current_city_min_cost_out[city] == -1:
                current_city_min_cost_out[city] = cost
                covered_count_out += 1
                total_depart_cost += cost
            else:
                if cost < current_city_min_cost_out[city]:
                    total_depart_cost -= current_city_min_cost_out[city]
                    current_city_min_cost_out[city] = cost
                    total_depart_cost += cost
        
        if covered_count_out == n:
            min_depart_cost[d] = total_depart_cost
            
    # Now find the optimal L
    # L is the day by which everyone must arrive.
    # Then they work L+1 ... L+k.
    # They must depart on day >= L+k+1.
    # So we need min_arrive_cost[L] + min_depart_cost[L+k+1]
    
    ans = float('inf')
    
    # L can range from 1 to MAX_DAY - k - 1 (since L+k+1 must be <= MAX_DAY roughly)
    # Actually, min_depart_cost is computed up to MAX_DAY-1.
    # The max day index is MAX_DAY-1.
    # So L+k+1 must be <= MAX_DAY-1? 
    # The loop for min_depart_cost goes down to 1.
    # If L+k+1 >= MAX_DAY, then min_depart_cost[L+k+1] is inf (since array size is MAX_DAY, indices 0..MAX_DAY-1).
    # Wait, MAX_DAY = 1000005. Days are up to 10^6.
    # So indices 1 to 1000000 are valid.
    # If L+k+1 > 1000000, then it's impossible to depart? 
    # The problem says d_i <= 10^6. So no flights after 10^6.
    # So if L+k+1 > 10^6, then min_depart_cost will be inf.
    
    for L in range(1, MAX_DAY):
        arrive_cost = min_arrive_cost[L]
        depart_day = L + k + 1
        if depart_day >= MAX_DAY:
            continue
        depart_cost = min_depart_cost[depart_day]
        
        if arrive_cost != float('inf') and depart_cost != float('inf'):
            if arrive_cost + depart_cost < ans:
                ans = arrive_cost + depart_cost
                
    if ans == float('inf'):
        print("-1")
    else:
        print(ans)

if __name__ == '__main__':
    solve()