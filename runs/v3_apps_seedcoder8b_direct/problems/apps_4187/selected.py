def max_continuous_rest(n, schedule):
    # Find the longest continuous sequence of 1s in the schedule
    max_rest = 0
    current_rest = 0
    
    # First pass to find the longest sequence in the original schedule
    for i in range(n):
        if schedule[i] == 1:
            current_rest += 1
            max_rest = max(max_rest, current_rest)
        else:
            current_rest = 0
    
    # Second pass to check if the sequence wraps around the end to the start
    if schedule[0] == 1 and schedule[-1] == 1:
        current_rest = 0
        for i in range(n):
            if schedule[i] == 1:
                current_rest += 1
            else:
                break
        for i in range(n-1, -1, -1):
            if schedule[i] == 1:
                current_rest += 1
            else:
                break
        max_rest = max(max_rest, current_rest)
    
    return max_rest

# Read input
n = int(input().strip())
schedule = list(map(int, input().strip().split()))

# Output the result
print(max_continuous_rest(n, schedule))