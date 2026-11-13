def min_power_task(n, k, a):
    # Calculate the number of tasks Dima can do between Inna's tells
    tasks_between_tells = k - 1
    
    # Initialize the minimum power and the best starting task
    min_power = float('inf')
    best_start_task = 1
    
    # Iterate over each possible starting task
    for start in range(n):
        current_power = 0
        # Calculate the power Dima gets told off with if he starts at this task
        for i in range(tasks_between_tells):
            task_index = (start + i) % n
            current_power += a[task_index]
        
        # Update the minimum power and best starting task if a lower power is found
        if current_power < min_power:
            min_power = current_power
            best_start_task = start + 1
    
    return best_start_task

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
a = list(map(int, data[2:2 + n]))

# Get the result and print it
result = min_power_task(n, k, a)
print(result)