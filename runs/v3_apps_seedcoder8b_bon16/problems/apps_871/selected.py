def find_takeoff_time(n, s, landings):
    def time_to_minutes(h, m):
        return h * 60 + m

    def minutes_to_time(m):
        return divmod(m, 60)

    current_time = 0
    for h, m in landings:
        landing_time = time_to_minutes(h, m)
        if landing_time - current_time >= 2 * s + 1:
            return minutes_to_time(current_time + s)
        current_time = landing_time + 1

    # If we can't insert between landings, add after the last one
    return minutes_to_time(current_time + s)

def main():
    n, s = map(int, input().split())
    landings = [tuple(map(int, input().split())) for _ in range(n)]
    
    h, m = find_takeoff_time(n, s, landings)
    print(h, m)

if __name__ == "__main__":
    main()