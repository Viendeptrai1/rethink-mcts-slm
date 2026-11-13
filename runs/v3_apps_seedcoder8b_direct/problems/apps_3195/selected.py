def traffic_light_probability():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    # Read the durations of the traffic light cycle
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
    
    # Determine the possible starting times T
    possible_starts = []
    for t, c in observations:
        if c == 'green':
            possible_starts.append(t)
        elif c == 'yellow':
            possible_starts.append(t - T_g)
        elif c == 'red':
            possible_starts.append(t - T_g - T_y)
    
    # Function to determine the color at time t given a start time T
    def get_color_at_time(T, t):
        cycle_time = (t - T) % (T_g + T_y + T_r)
        if 0 <= cycle_time < T_g:
            return 'green'
        elif T_g <= cycle_time < T_g + T_y:
            return 'yellow'
        else:
            return 'red'
    
    # Count how many times the color c_q appears at time t_q
    count_c_q_at_t_q = 0
    for T in possible_starts:
        if get_color_at_time(T, t_q) == c_q:
            count_c_q_at_t_q += 1
    
    # Calculate the probability
    probability = count_c_q_at_t_q / len(possible_starts)
    
    # Print the result
    print(f"{probability:.6f}")