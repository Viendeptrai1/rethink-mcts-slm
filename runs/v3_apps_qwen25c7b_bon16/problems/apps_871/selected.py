from datetime import datetime, timedelta

def earliest_takeoff_time(n, s, landings):
    def time_to_minutes(h, m):
        return h * 60 + m
    
    def minutes_to_time(minutes):
        return divmod(minutes, 60)
    
    landings = [(time_to_minutes(h, m), h, m) for h, m in landings]
    landings.append((time_to_minutes(24, 0), 24, 0))
    
    min_time = float('inf')
    best_hour, best_minute = -1, -1
    
    for i in range(n + 1):
        if i > 0:
            prev_landing_time, _, _ = landings[i-1]
            if prev_landing_time < time_to_minutes(23, 59) - s:
                gap_start = max(prev_landing_time + s, time_to_minutes(0, 0))
            else:
                gap_start = time_to_minutes(24, 0)
            
            if gap_start < time_to_minutes(24, 0):
                gap_end = gap_start + 1
                if gap_end > time_to_minutes(23, 59):
                    gap_end -= 24 * 60
                
                if gap_end < min_time:
                    min_time = gap_end
                    best_hour, best_minute = minutes_to_time(gap_start)
        
        if i < n:
            curr_landing_time, _, _ = landings[i]
            if curr_landing_time > s:
                gap_start = 0
            else:
                gap_start = s - curr_landing_time
            
            gap_end = gap_start + 1
            if gap_end > time_to_minutes(23, 59):
                gap_end -= 24 * 60
            
            if gap_end < min_time:
                min_time = gap_end
                best_hour, best_minute = minutes_to_time(gap_start)
    
    return best_hour, best_minute

# Input reading
n, s = map(int, input().split())
landings = [tuple(map(int, input().split())) for _ in range(n)]

# Output result
print(*earliest_takeoff_time(n, s, landings))