import sys
import heapq

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        M = int(next(iterator))
    except StopIteration:
        return

    trains = []
    for _ in range(M):
        x = int(next(iterator))
        s = int(next(iterator))
        t = int(next(iterator))
        l = int(next(iterator))
        trains.append((x, s, t, l))

    # We only care about trains starting at station 1
    trains_from_1 = [t for t in trains if t[0] == 1]
    
    # If there are no trains from station 1, impossible
    if not trains_from_1:
        print("impossible")
        return

    # Sort trains by departure time
    trains_from_1.sort(key=lambda x: x[1])

    # Precompute the earliest arrival time at station N for any given departure time from station 1.
    # Since we can only take trains from station 1 to 2, then 2 to 3, etc., and we start at station 1,
    # the path is deterministic in terms of stations visited (1->2->3->...->N).
    # However, we can choose which train to take for each leg.
    # To find the "worst-case" (fastest) arrival for a specific start time T_start:
    # We simulate the journey greedily: at each station i (from 1 to N-1), we take the earliest arriving train
    # that departs at or after our current arrival time at station i.
    
    # Let's precompute for each station i, the list of trains going from i to i+1, sorted by departure time.
    trains_by_station = [[] for _ in range(N)]
    for t in trains:
        trains_by_station[t[0]].append(t)
    
    # Sort each list by departure time
    for i in range(N):
        trains_by_station[i].sort(key=lambda x: x[1])

    # Function to find earliest arrival at station N given start time at station 1
    def get_earliest_arrival(start_time):
        current_time = start_time
        current_station = 1
        
        # We need to reach station N
        for station in range(1, N):
            # Find the earliest train from 'station' to 'station+1' that departs >= current_time
            # Since the list is sorted, we can use binary search or linear scan (N is small, M is large but we do this N times)
            # Actually, we can optimize by maintaining a pointer, but N is only 100, so linear scan over filtered trains is fine.
            # However, M is 10^5, so we should be careful. But we only do this N times (100), and each scan is over M trains? 
            # No, we can filter once. Let's just use bisect or a simple loop since we sort once.
            
            # Find trains from current_station
            station_trains = trains_by_station[station]
            
            # Find first train with departure >= current_time
            # Using bisect_left on departure times
            import bisect
            dep_times = [t[1] for t in station_trains]
            
            idx = bisect.bisect_left(dep_times, current_time)
            
            if idx == len(station_trains):
                # No train available from this station after current_time
                return float('inf')
            
            # Take the earliest available train
            chosen_train = station_trains[idx]
            # Arrival time at next station
            # The train's planned arrival is t, but it is delayed by l.
            # So actual arrival = t + l
            current_time = chosen_train[2] + chosen_train[3]
            current_station += 1
            
        return current_time

    # We need to check every possible start time that corresponds to a train departure from station 1.
    # The problem asks for the earliest start time (train departure) such that:
    # (Earliest Arrival Time) - (Hypothetical On-Time Arrival Time) >= 1800
    #
    # What is the "Hypothetical On-Time Arrival Time"?
    # The problem says: "of the time you would have arrived assuming your booked journey was exactly on time."
    # This phrasing is slightly ambiguous. Does it mean:
    # 1. If we took the SAME train but with 0 delay, when would we arrive?
    # 2. Or does it mean the arrival time if the entire journey was perfect?
    #
    # Re-reading: "no matter the combination of trains you had taken ... you would still be unable to reach your destination in strictly less time than 30 minutes (or 1800 seconds), of the time you would have arrived assuming your booked journey was exactly on time."
    #
    # Interpretation: 
    # Let T_start be the departure time of the train we book.
    # Let T_arr_actual be the actual arrival time at station N (with all delays).
    # Let T_arr_on_time be the arrival time at station N if the specific train we booked had 0 delay (and subsequent trains also had 0 delay? Or just the first one?).
    #
    # "assuming your booked journey was exactly on time" likely refers to the specific train instance we booked having its scheduled times (S, T) instead of (S+L, T+L).
    # But what about the rest of the journey? "no matter the combination of trains you had taken". This implies we are comparing the actual path (with delays) to a hypothetical path where ONLY the booked train is on time, and the rest of the choices (and their delays) remain the same? 
    # OR, does it mean we compare the actual arrival to the arrival if EVERYTHING was on time?
    #
    # Let's look at the condition: "unable to reach your destination in strictly less time than 1800 seconds, of the time you would have arrived assuming your booked journey was exactly on time."
    # This means: (Actual Arrival) - (Hypothetical Arrival) >= 1800.
    #
    # Hypothesis: The "booked journey" refers to the specific train leg from 1 to 2. 
    # If we book train i (depart S, arrive T, delay L), then:
    # Actual arrival at station 2 = T + L.
    # Hypothetical arrival at station 2 = T (since it's on time).
    # Then from station 2 to N, we take the same sequence of trains (same delays) as in the actual scenario? 
    # If so, the difference in arrival at N would be exactly L (the delay of the first train).
    # Then the condition becomes: L >= 1800.
    # But the problem says "no matter the combination of trains you had taken". This suggests the path might vary.
    #
    # Alternative Interpretation (more likely for "ruthless capitalist" puzzle):
    # The "booked journey" defines the START time. The "time you would have arrived assuming your booked journey was exactly on time" means:
    # If we started at the same time T_start, but the train was on time (so we arrived at station 2 at T instead of T+L), and then we took the BEST possible path from station 2 to N (with all delays as given in the input)?
    # No, that doesn't fit "assuming your booked journey was exactly on time".
    #
    # Let's reconsider the wording carefully: "of the time you would have arrived assuming your booked journey was exactly on time."
    # This usually implies a counterfactual: "If the train I booked had run on schedule, when would I have arrived?"
    # In that counterfactual, the delay L of the booked train is 0. What about other trains? 
    # "no matter the combination of trains you had taken" -> This clause modifies the condition "unable to reach...". It means: Even if you took the fastest possible combination of trains (given the delays), you still wouldn't arrive < 1800s after the on-time baseline.
    #
    # So:
    # Baseline Arrival (On-Time): Start at T_start. Take the booked train (on time, so arrive station 2 at T). Then from station 2, take the FASTEST possible path to N using the given delayed trains.
    # Actual Arrival: Start at T_start. Take the booked train (delayed, arrive station 2 at T+L). Then from station 2, take the FASTEST possible path to N using the given delayed trains.
    #
    # Wait, if we take the fastest path from station 2 in both cases, the only difference is the arrival time at station 2.
    # Case 1 (On-Time): Arrive station 2 at T. Then fastest path from T to N.
    # Case 2 (Delayed): Arrive station 2 at T+L. Then fastest path from T+L to N.
    #
    # The condition is: (Fastest Arrival from T+L) - (Fastest Arrival from T) >= 1800.
    #
    # This makes sense. The "combination of trains" refers to the optimal choices made from station 2 onwards. We want to ensure that even with optimal play from station 2, the delay L pushes us back by at least 1800 seconds relative to the on-time baseline.
    #
    # Algorithm:
    # 1. For each train departing from station 1 (candidate start time T_start = S, planned arrival T, delay L):
    #    a. Calculate A1 = Earliest arrival at N starting from station 2 at time T (using all available trains with their delays).
    #    b. Calculate A2 = Earliest arrival at N starting from station 2 at time T+L (using all available trains with their delays).
    #    c. If A2 - A1 >= 1800, then this train is a valid candidate.
    # 2. Among all valid candidates, pick the one with the smallest T_start (S).
    # 3. If none, output "impossible".
    
    # We need a function: earliest_arrival_at_N(start_station, start_time)
    # This is similar to get_earliest_arrival but starting from an arbitrary station.
    
    def earliest_arrival_at_N(start_station, start_time):
        current_time = start_time
        current_station = start_station
        
        for station in range(start_station, N):
            station_trains = trains_by_station[station]
            dep_times = [t[1] for t in station_trains]
            
            idx = bisect.bisect_left(dep_times, current_time)
            
            if idx == len(station_trains):
                return float('inf')
            
            chosen_train = station_trains[idx]
            current_time = chosen_train[2] + chosen_train[3]
            current_station += 1
            
        return current_time

    best_start_time = float('inf')
    found = False

    for train in trains_from_1:
        s = train[1]
        t = train[2]
        l = train[3]
        
        # Baseline: arrive at station 2 at time t (on time)
        arrival_on_time = earliest_arrival_at_N(2, t)
        
        # Actual: arrive at station 2 at time t + l
        arrival_delayed = earliest_arrival_at_N(2, t + l)
        
        if arrival_on_time == float('inf') or arrival_delayed == float('inf'):
            continue
            
        diff = arrival_delayed - arrival_on_time
        if diff >= 1800:
            if s < best_start_time:
                best_start_time = s
            found = True

    if found:
        print(best_start_time)
    else:
        print("impossible")

if __name__ == "__main__":
    solve()