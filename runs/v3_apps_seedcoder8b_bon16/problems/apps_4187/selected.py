def max_continuous_rest(n, schedule):
    max_rest = 0
    current_rest = 0
    start_rest = 0
    
    for i in range(n * 2):
        if schedule[i % n] == 1:
            current_rest += 1
        else:
            if current_rest > max_rest:
                max_rest = current_rest
                start_rest = i % n - current_rest + 1
            current_rest = 0
        
        if i >= n and schedule[i % n] == 1 and schedule[(i - 1) % n] == 0:
            break
    
    return max_rest

# Read input
n = int(input())
schedule = list(map(int, input().split()))

# Calculate and print result
result = max_continuous_rest(n, schedule)
print(result)