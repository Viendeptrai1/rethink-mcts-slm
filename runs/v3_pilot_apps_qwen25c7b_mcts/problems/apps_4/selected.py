def min_snooze(x, hh, mm):
    target_minutes = hh * 60 + mm
    current_time = target_minutes
    
    while True:
        current_hour = current_time // 60 % 24
        current_minute = current_time % 60
        
        if '7' in str(current_hour) or '7' in str(current_minute):
            return (target_minutes - current_time) // x
        
        current_time -= x

# Example usage:
x = int(input())
hh, mm = map(int, input().split())
print(min_snooze(x, hh, mm))