import sys

def find_earliest_takeoff_time(n, s, landings):
    def time_to_minutes(h, m):
        return h * 60 + m

    def minutes_to_time(minutes):
        h = minutes // 60
        m = minutes % 60
        return h, m

    # Add a dummy landing at the end to handle the case where takeoff can be after the last landing
    landings.append((24, 0))
    landings_minutes = [time_to_minutes(h, m) for h, m in landings]

    for i in range(len(landings_minutes) - 1):
        current_landing = landings_minutes[i]
        next_landing = landings_minutes[i + 1]
        
        # Check if we can fit the takeoff between current_landing and next_landing
        if next_landing - current_landing > 2 * s + 1:
            takeoff_time = current_landing + s + 1
            return minutes_to_time(takeoff_time)
    
    # If no suitable time found, return the time after the last landing
    return minutes_to_time(landings_minutes[-1])

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
    
    h, m = find_earliest_takeoff_time(n, s, landings)
    print(h, m)

if __name__ == "__main__":
    main()