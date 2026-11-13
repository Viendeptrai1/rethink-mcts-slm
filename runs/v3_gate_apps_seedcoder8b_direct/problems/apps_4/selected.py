def find_minimum_snoozes(x, hh, mm):
    def is_lucky_time(h, m):
        return '7' in f"{h:02}{m:02}"

    # Convert the wake-up time to minutes since midnight
    wake_up_minutes = hh * 60 + mm

    # Start checking from the current time
    current_minutes = wake_up_minutes
    snooze_count = 0

    while True:
        # Calculate the current hour and minute
        current_hh = (current_minutes // 60) % 24
        current_mm = current_minutes % 60

        # Check if the current time is lucky
        if is_lucky_time(current_hh, current_mm):
            return snooze_count

        # Press snooze and move to the next alarm time
        current_minutes -= x
        snooze_count += 1

# Read input
x = int(input().strip())
hh, mm = map(int, input().strip().split())

# Find and print the minimum number of snoozes
print(find_minimum_snoozes(x, hh, mm))