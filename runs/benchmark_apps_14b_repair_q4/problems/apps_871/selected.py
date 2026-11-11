import sys

def find_earliest_takeoff_time(n, s, landings):
    # Convert landing times to minutes since start
    landing_times = [h * 60 + m for h, m in landings]
    
    # Check if we can place the takeoff before the first landing
    if landing_times[0] >= s + 1:
        return (0, 0)
    
    # Check between each pair of landings
    for i in range(1, n):
        if landing_times[i] - landing_times[i - 1] >= 2 * s + 1:
            return (landing_times[i - 1] // 60 + (landing_times[i - 1] % 60 + s + 1) // 60, 
                    (landing_times[i - 1] % 60 + s + 1) % 60)
    
    # Check after the last landing
    if 24 * 60 - landing_times[-1] >= s + 1:
        return (landing_times[-1] // 60 + 1, 0)
    
    # If no valid time found, return the next day
    return (24, 0)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    s = int(data[1])
    landings = []
    
    for i in range(n):
        h = int(data[2 + 2 * i])
        m = int(data[3 + 2 * i])
        landings.append((h, m))
    
    result = find_earliest_takeoff_time(n, s, landings)
    print(result[0], result[1])

if __name__ == "__main__":
    main()