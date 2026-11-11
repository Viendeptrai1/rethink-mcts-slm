def increment_time(time):
    h, m = map(int, time.split(':'))
    m += 1
    if m == 60:
        m = 0
        h += 1
        if h == 24:
            h = 0
    return f"{h:02}:{m:02}"

def decrement_time(time):
    h, m = map(int, time.split(':'))
    m -= 1
    if m == -1:
        m = 59
        h -= 1
        if h == -1:
            h = 23
    return f"{h:02}:{m:02}"

def valid_times(start, end):
    times = set()
    current = start
    while current != end:
        times.add(current)
        current = increment_time(current)
    times.add(end)
    return sorted(times)

def main():
    import sys
    input = sys.stdin.read
    data = input().splitlines()
    
    original_time = data[0]
    current_time = data[1]
    
    if original_time == current_time:
        print(1)
        print(original_time)
        return
    
    times = valid_times(original_time, current_time)
    print(len(times))
    for time in times:
        print(time)

if __name__ == "__main__":
    main()