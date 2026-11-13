def max_path_length(v1, v2, t, d):
    if v1 == v2:
        return v1 * t
    
    if abs(v1 - v2) > d * (t - 1):
        return -1
    
    if v1 < v2:
        start_speed = v1
        end_speed = v2
    else:
        start_speed = v2
        end_speed = v1
    
    max_length = 0
    current_speed = start_speed
    
    while current_speed != end_speed:
        if current_speed < end_speed:
            current_speed += min(d, end_speed - current_speed)
        else:
            current_speed -= min(d, current_speed - end_speed)
        
        max_length += current_speed
    
    max_length += end_speed
    
    return max_length

# Example usage:
v1, v2 = map(int, input().split())
t, d = map(int, input().split())
print(max_path_length(v1, v2, t, d))