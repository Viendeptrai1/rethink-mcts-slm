from collections import deque

def find_times_to_set_clock(original_time, target_time):
    def time_to_minutes(time_str):
        hh, mm = map(int, time_str.split(':'))
        return hh * 60 + mm

    def minutes_to_time(minutes):
        hh = minutes // 60
        mm = minutes % 60
        return f"{hh:02}:{mm:02}"

    def neighbors(minutes):
        hh, mm = divmod(minutes, 60)
        for i in range(4):
            digit = (minutes // (10 ** i)) % 10
            for change in (-1, 1):
                new_digit = (digit + change) % 10
                new_minutes = minutes - (digit - new_digit) * (10 ** i)
                if i < 2:  # hour part
                    new_hh = new_minutes // 60
                    if 0 <= new_hh < 24:
                        yield new_minutes
                else:  # minute part
                    new_mm = new_minutes % 60
                    if 0 <= new_mm < 60:
                        yield new_minutes

    original_minutes = time_to_minutes(original_time)
    target_minutes = time_to_minutes(target_time)

    queue = deque([(original_minutes, [original_time])])
    visited = set([original_minutes])

    while queue:
        current_minutes, path = queue.popleft()
        if current_minutes == target_minutes:
            return len(path), path

        for neighbor in neighbors(current_minutes):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [minutes_to_time(neighbor)]))

    return 0, []

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().strip().split()
    original_time = data[0]
    target_time = data[1]
    count, times = find_times_to_set_clock(original_time, target_time)
    print(count)
    for time in times:
        print(time)