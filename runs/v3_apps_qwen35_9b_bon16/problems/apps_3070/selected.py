import sys

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
        X = int(next(iterator))
        S = int(next(iterator))
        T = int(next(iterator))
        L = int(next(iterator))
        trains.append((X, S, T, L))

    # We are only concerned with trains starting at station 1 (X=1)
    # because we need to book a journey from station 1.
    # The problem states: "Each train goes between stations X and X+1."
    # And we start at station 1. So we look for trains where X == 1.

    # Condition for compensation:
    # Let T_on_time be the arrival time at the destination (station 2) if the train was exactly on schedule.
    # Let T_arrival be the actual arrival time with delay L.
    # T_arrival = T_on_time + L.
    # We earn compensation if T_arrival >= 1800 + T_on_time.
    # Substituting: T_on_time + L >= 1800 + T_on_time
    # This simplifies to L >= 1800.
    #
    # Wait, let's re-read carefully: "you would still be unable to reach your destination in strictly less time than 30 minutes (or 1800 seconds), of the time you would have arrived assuming your booked journey was exactly on time."
    #
    # Let t_real be the actual time you arrive at the destination.
    # Let t_planned be the time you would have arrived if the train was on time.
    # The condition is: t_real >= t_planned + 1800.
    #
    # Given input: S (planned start), T (planned end), L (delay).
    # Actual start = S + L.
    # Actual end = T + L.
    # So t_real = T + L.
    # t_planned = T.
    # Condition: T + L >= T + 1800  => L >= 1800.
    #
    # However, there is a constraint: "provided that no matter the combination of trains you had taken (provided they followed the same route of stations as planned), you would still be unable to reach your destination in strictly less time than 30 minutes... of the time you would have arrived assuming your booked journey was exactly on time."
    #
    # This phrasing is tricky. "no matter the combination of trains you had taken".
    # If I book a train that is delayed, can I switch to another train at an intermediate station to arrive earlier?
    # But the route is fixed: Station 1 -> Station 2 -> ... -> Station N.
    # Since we are only looking for a journey from Station 1, and the input says "Each train goes between stations X and X+1", this implies a linear path 1->2->3...->N.
    # If I take a train from 1 to 2, I am now at station 2. If I want to go to station N, I must continue.
    # But the problem asks: "what is the earliest time you can book a train for from station 1".
    # This implies we are considering a single trip from 1 to 2? Or 1 to N?
    # "reach your destination". If the destination is N, and we only have trains between X and X+1, we need a sequence of trains.
    # However, the input gives M trains, not necessarily covering the whole path, but the problem says "provided they followed the same route of stations as planned".
    #
    # Let's reconsider the "no matter the combination" part.
    # If I book a train with delay L1, my planned arrival is T1. My actual arrival is T1 + L1.
    # The condition is T1 + L1 >= T1 + 1800 => L1 >= 1800.
    # But what if I change trains? Suppose at station 2, I take a train with delay L2.
    # The "combination of trains" suggests we are looking at the total journey time.
    # Total Planned Time = Sum(Planned Durations).
    # Total Actual Time = Sum(Planned Durations) + Sum(Delays).
    # The condition "unable to reach ... in strictly less time than 1800 seconds OF the time you would have arrived assuming ... on time" usually means:
    # Actual Arrival Time - Planned Arrival Time >= 1800.
    # Which simplifies to Sum(Delays) >= 1800.
    #
    # BUT, the phrase "no matter the combination of trains you had taken" implies robustness against transfers.
    # If I book a train at Station 1, I might transfer at Station 2, 3, etc.
    # If there exists ANY valid combination of trains (respecting the delays and connections) that gets me to the destination in < Planned_Arrival + 1800, then I do NOT get compensation.
    # I get compensation ONLY IF ALL possible valid combinations result in arrival >= Planned_Arrival + 1800.
    #
    # Let's model this as a shortest path problem on a graph of stations and time.
    # Nodes: (station, time).
    # Edges: Trains. A train from X to X+1 with planned S, T, and delay L allows travel from (X, S+L) to (X+1, T+L).
    # Wait, the constraint is on the arrival time relative to the planned arrival of the specific booked journey?
    # Or relative to the planned arrival of the optimal combination?
    # "of the time you would have arrived assuming your booked journey was exactly on time."
    # This refers to the specific train we book at Station 1. Let's call its planned arrival P_arr.
    # We need: Actual_Arrival >= P_arr + 1800.
    # Actual_Arrival depends on the path taken.
    # Let the path be T1, T2, ..., Tk.
    # T1 is the train we book from Station 1. Its planned arrival is P_arr.
    # The actual arrival time is sum of actual durations.
    # Actual_Arrival = P_arr + Sum(L_i for all i in path).
    # So the condition becomes: P_arr + Sum(L_i) >= P_arr + 1800 => Sum(L_i) >= 1800.
    #
    # So, if we book train T1, we get compensation if and only if for ALL valid paths starting with T1, the sum of delays on that path is >= 1800.
    # Equivalently, the minimum sum of delays over all valid paths starting with T1 must be >= 1800.
    #
    # Algorithm:
    # 1. Identify all trains starting at Station 1. These are candidates for the first leg.
    # 2. For each candidate train T1 (with delay L1), we need to check if there exists a path from Station 2 to N such that L1 + Sum(L_other) < 1800.
    #    If such a path exists, then this T1 is NOT a valid booking (because we could take that path and get < 1800 extra delay, failing the condition).
    #    If for a given T1, ALL paths from Station 2 to N have Sum(L_other) >= 1800 - L1, then T1 is valid.
    #    Actually, simpler: We need min(Sum of delays from Station 2 to N) >= 1800 - L1.
    #    If the shortest delay path from Station 2 to N is D_min, then we need L1 + D_min >= 1800.
    #    If L1 + D_min < 1800, then there exists a combination (T1 + that path) that results in < 1800 total delay, so we don't get compensation.
    #    If L1 + D_min >= 1800, then all combinations (since D_min is the minimum) will have total delay >= 1800, so we DO get compensation.
    #
    # 3. We want the earliest start time S among all valid trains T1.
    # 4. If no train satisfies the condition, output "impossible".

    # Steps:
    # 1. Build a graph where nodes are stations 1..N.
    # 2. Edges are trains. For each train (X, S, T, L), add a directed edge X -> X+1 with weight L.
    #    Note: The weight is the delay L. We want to find the path with minimum total weight.
    # 3. Compute the shortest path (minimum total delay) from Station 2 to Station N. Let this be min_delay_suffix.
    #    If Station 2 and Station N are disconnected, then it's impossible to complete the journey after the first leg. 
    #    In that case, is the condition satisfied? 
    #    "no matter the combination of trains you had taken ... you would still be unable to reach".
    #    If you cannot reach the destination, you definitely don't reach it in < 1800 seconds.
    #    So if Station 2 -> N is unreachable, then any train from 1 is valid? 
    #    Yes, because there is no combination that allows you to reach the destination, so the condition "unable to reach" is trivially true for all combinations (since there are none that succeed).
    #    Wait, "unable to reach your destination in strictly less time than 30 minutes ... of the time you would have arrived".
    #    If you never arrive, you certainly don't arrive in < Planned + 1800.
    #    So if 2->N is disconnected, all trains from 1 are valid candidates.
    #
    # 4. Iterate through all trains starting at Station 1.
    #    For each train with delay L:
    #       If 2->N is unreachable: Valid.
    #       Else: Check if L + min_delay_suffix >= 1800.
    #       If yes, record the start time S.
    #
    # 5. Find the minimum S among valid trains. If none, print "impossible".

    # Dijkstra's algorithm for shortest path on delays (weights are non-negative).
    # Stations: 1 to N.
    # We need min distance from 2 to N.
    # Since edges go X -> X+1, the graph is a DAG (Directed Acyclic Graph) based on station index.
    # We can simply use DP or Dijkstra. Dijkstra is safer and easy to implement.
    # Actually, since it's a line 1->2->3...->N, we can just iterate from 2 to N and compute min cost.
    # But wait, multiple trains might exist between X and X+1. We take the one with min delay for the shortest path?
    # Yes, for the suffix sum, we just need the minimum total delay path.
    # Since we can switch trains at any station, at each station X (for X > 1), we want to arrive at X+1 with minimum cumulative delay.
    # Let dp[x] = minimum total delay to reach station x from station 2.
    # dp[2] = 0.
    # For x from 2 to N-1:
    #   Find all trains from x to x+1.
    #   dp[x+1] = min(dp[x+1], dp[x] + L_train)
    #
    # Wait, is it possible to wait? "It is possible to change between trains instantanesouly."
    # Waiting doesn't reduce delay. Delay is fixed per train. So we just want the path with sum of L's minimized.
    # Since the graph is a line (only edges X->X+1), the path is unique in terms of stations, but we have choices of trains.
    # So at each step X->X+1, we pick the train with the smallest L.
    # So min_delay_suffix = sum(min(L) for each segment 2->3, 3->4, ..., N-1->N).
    # If any segment has no trains, then the path is broken (unreachable).

    # Let's refine:
    # min_delays[i] = minimum delay to go from station i to i+1. If no train, infinity.
    # Total min delay from 2 to N = sum(min_delays[i] for i in 2..N-1).
    # If any min_delay is infinity, then 2->N is unreachable.

    min_seg_delays = {} # key: station index X, value: min delay X->X+1
    INF = float('inf')

    for train in trains:
        X, S, T, L = train
        if X in min_seg_delays:
            if L < min_seg_delays[X]:
                min_seg_delays[X] = L
        else:
            min_seg_delays[X] = L

    # Check connectivity from 2 to N
    # We need segments 2, 3, ..., N-1
    total_min_suffix = 0
    possible_suffix = True
    for i in range(2, N):
        if i not in min_seg_delays:
            possible_suffix = False
            break
        total_min_suffix += min_seg_delays[i]

    valid_train_start_times = []

    for train in trains:
        X, S, T, L = train
        if X != 1:
            continue
        
        # Check condition
        if not possible_suffix:
            # If suffix is unreachable, any train from 1 is valid
            valid_train_start_times.append(S)
        else:
            if L + total_min_suffix >= 1800:
                valid_train_start_times.append(S)

    if not valid_train_start_times:
        print("impossible")
    else:
        print(min(valid_train_start_times))

if __name__ == "__main__":
    solve()

```