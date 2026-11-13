def find_minimum_snoozes(x, hh, mm):
    def is_lucky(time):
        return '7' in time

    def time_to_minutes(h, m):
        return h * 60 + m

    def minutes_to_time(m):
        h = (m // 60) % 24
        m = m % 60
        return f"{h:02}:{m:02}"

    wake_up_minutes = time_to_minutes(hh, mm)
    snooze_count = 0

    while True:
        alarm_time_minutes = wake_up_minutes - snooze_count * x
        if alarm_time_minutes < 0:
            alarm_time_minutes += 24 * 60
        alarm_time = minutes_to_time(alarm_time_minutes)

        if is_lucky(alarm_time):
            return snooze_count

        snooze_count += 1

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().strip().split()
    x = int(data[0])
    hh = int(data[1])
    mm = int(data[2])
    print(find_minimum_snoozes(x, hh, mm))