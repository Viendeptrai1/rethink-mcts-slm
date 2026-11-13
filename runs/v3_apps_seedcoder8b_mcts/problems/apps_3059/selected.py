def expected_time_to_set_record():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    r = int(data[1])
    m = int(data[2])
    
    tricks = []
    index = 3
    for _ in range(m):
        t = int(data[index])
        p = float(data[index + 1])
        d = int(data[index + 2])
        tricks.append((t, p, d))
        index += 3
    
    # Initialize expected time to complete the run without any resets
    expected_time = n
    
    # Calculate expected time to set a new record
    for i in range(m):
        t, p, d = tricks[i]
        
        # Expected time to complete the run from the start to the current trick
        time_to_trick = t if i == 0 else tricks[i-1][0] + tricks[i-1][2]
        
        # Expected time to fail the trick
        expected_failure_time = time_to_trick + d
        
        # Expected time to complete the run from the current trick
        remaining_time = n - t
        
        # Expected time if we reset after the current trick
        expected_time_with_reset = expected_failure_time + remaining_time
        
        # Update the expected time to be the minimum of the current expected time
        # and the expected time with reset after the current trick
        expected_time = min(expected_time, expected_time_with_reset)
    
    print(expected_time)