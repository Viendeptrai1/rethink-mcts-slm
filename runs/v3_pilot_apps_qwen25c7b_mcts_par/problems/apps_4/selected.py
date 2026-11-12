from sys import stdin, stdout

def find_snooze_presses(x, hh, mm):
    target_minutes = hh * 60 + mm
    current_time = target_minutes
    
    while True:
        current_hour = current_time // 60 % 24
        current_minute = current_time % 60
        
        if '7' in str(current_hour) or '7' in str(current_minute):
            return (target_minutes - current_time) // x
        
        current_time -= x

# Read input
x = int(stdin.readline().strip())
hh, mm = map(int, stdin.readline().strip().split())

# Output result
stdout.write(str(find_snooze_presses(x, hh, mm)) + '\n')