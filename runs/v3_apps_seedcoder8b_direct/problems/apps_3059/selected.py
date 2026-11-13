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
    
    # Calculate expected time with resets
    current_time = 0
    for t, p, d in tricks:
        # Time to reach this trick
        time_to_trick = t - current_time
        
        # Expected time to fail this trick
        expected_failure_time = time_to_trick + d
        
        # Expected time to succeed this trick
        expected_success_time = time_to_trick
        
        # Update expected time considering reset strategy
        expected_time += min(expected_failure_time, expected_success_time / p)
        
        # Update current time to the time after this trick
        current_time = t
    
    # Print the result with required precision
    print(f"{expected_time:.10f}")