def minimum_power_task(n, k, a):
    min_power = float('inf')
    best_start = 0
    
    # The number of tasks Dima can do in between each Inna's telling off session
    tasks_between_tells = (n // k) - 1
    
    # Iterate over each possible starting task
    for start in range(n):
        power = 0
        # Calculate the power Dima would incur if starting from this task
        for i in range(1, tasks_between_tells + 1):
            power += a[(start + i * k) % n]
        
        # Check if this starting point gives a lower power, or if it's equal and starts earlier
        if power < min_power:
            min_power = power
            best_start = start + 1  # Convert to 1-based index
    
    return best_start

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    a = list(map(int, data[2:n+2]))
    
    result = minimum_power_task(n, k, a)
    print(result)