import sys
import math

def expected_time_to_beat_record():
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
    
    def compute_expected_time():
        # Initialize the expected time with the time for a successful run without any tricks
        expected_time = n
        
        # Go through each trick
        for i, (t, p, d) in enumerate(tricks):
            # Calculate the expected time if this trick fails
            if i == 0:
                time_before_trick = 0
            else:
                time_before_trick = tricks[i-1][0]
            
            expected_time_to_failure = time_before_trick + d * (1 - p)
            
            # Update the expected time with the minimum of the current expected time and the time if we reset after this trick
            expected_time = min(expected_time, expected_time_to_failure + n - t)
        
        return expected_time
    
    # Calculate and print the expected time
    result = compute_expected_time()
    print(result)