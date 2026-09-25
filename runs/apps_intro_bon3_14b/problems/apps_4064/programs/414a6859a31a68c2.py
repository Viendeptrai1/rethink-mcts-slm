import sys

def max_good_sleeping_times(n, h, l, r, a):
    current_time = 0
    good_sleeps = 0
    
    for i in range(n):
        # Calculate the two possible sleep times
        sleep_time1 = (current_time + a[i]) % h
        sleep_time2 = (current_time + a[i] - 1) % h
        
        # Choose the best option
        if l <= sleep_time1 <= r:
            good_sleeps += 1
            current_time = sleep_time1
        elif l <= sleep_time2 <= r:
            good_sleeps += 1
            current_time = sleep_time2
        else:
            # If neither is good, choose the one that gets closer to the next good time
            if abs(sleep_time1 - l) < abs(sleep_time2 - l):
                current_time = sleep_time1
            else:
                current_time = sleep_time2
    
    return good_sleeps

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
h = int(data[1])
l = int(data[2])
r = int(data[3])
a = list(map(int, data[4:]))

# Output the result
print(max_good_sleeping_times(n, h, l, r, a))