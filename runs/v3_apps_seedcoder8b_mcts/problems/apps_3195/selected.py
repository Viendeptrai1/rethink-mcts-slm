def calculate_probability():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    # Read the durations of the traffic light cycles
    T_g = int(data[0])
    T_y = int(data[1])
    T_r = int(data[2])
    
    # Read the number of observations
    n = int(data[3])
    
    # Read the observations
    observations = []
    index = 4
    for _ in range(n):
        t = int(data[index])
        c = data[index + 1]
        observations.append((t, c))
        index += 2
    
    # Read the query
    t_q = int(data[index])
    c_q = data[index + 1]
    
    # Determine the earliest possible start time T
    min_time_diff = float('inf')
    for i in range(1, n):
        time_diff = observations[i][0] - observations[i - 1][0]
        min_time_diff = min(min_time_diff, time_diff)
    
    # Calculate the cycle length
    cycle_length = T_g + T_y + T_r
    
    # Determine the possible start times T
    possible_starts = []
    for i in range(n - 1):
        time_diff = observations[i + 1][0] - observations[i][0]
        if time_diff == min_time_diff:
            possible_starts.append(observations[i][0])
    
    # Function to determine the color at time t given a start time T
    def get_color_at_time(T, t):
        time_since_start = (t - T) % cycle_length
        if time_since_start < T_g:
            return "green"
        elif time_since_start < T_g + T_y:
            return "yellow"
        else:
            return "red"
    
    # Count the number of times the color c_q appears at time t_q
    count_c_q = 0
    for T in possible_starts:
        if get_color_at_time(T, t_q) == c_q:
            count_c_q += 1
    
    # Calculate the probability
    probability = count_c_q / len(possible_starts)
    
    # Print the result
    print(f"{probability:.6f}")