import sys

def parse_time(h, m):
    return h * 60 + m

def format_time(minutes):
    h = minutes // 60
    m = minutes % 60
    return h, m

def find_earliest_takeoff(n, s, landings):
    current_time = 0
    for i in range(n):
        landing_time = parse_time(landings[i][0], landings[i][1])
        if i == 0:
            if landing_time >= s:
                return format_time(s)
        else:
            previous_landing_time = parse_time(landings[i-1][0], landings[i-1][1])
            if landing_time - previous_landing_time > 2 * s:
                return format_time(previous_landing_time + s)
    return format_time(current_time + s)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    s = int(data[1])
    landings = []
    index = 2
    for _ in range(n):
        h = int(data[index])
        m = int(data[index + 1])
        landings.append((h, m))
        index += 2
    
    result = find_earliest_takeoff(n, s, landings)
    print(result[0], result[1])

if __name__ == "__main__":
    main()