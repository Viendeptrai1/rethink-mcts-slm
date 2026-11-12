from sys import stdin, stdout

def min_snooze(x, hh, mm):
    target_time = hh * 60 + mm
    current_time = (hh * 60 + mm) % 1440  # Convert to 1440-minute cycle

    for i in range(1440 // x + 1):
        snooze_time = current_time - x * i
        if snooze_time < 0:
            snooze_time += 1440

        if '7' in str(snooze_time // 60).zfill(2) or '7' in str(snooze_time % 60).zfill(2):
            return i

# Read input
x = int(stdin.readline().strip())
hh, mm = map(int, stdin.readline().strip().split())

# Print result
stdout.write(str(min_snooze(x, hh, mm)) + '\n')