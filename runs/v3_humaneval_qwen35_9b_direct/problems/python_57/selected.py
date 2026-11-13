def monotonic(l: list):
    if len(l) <= 2:
        return True
    
    increasing = l[1] > l[0]
    decreasing = l[1] < l[0]
    
    if not increasing and not decreasing:
        return True
    
    for i in range(2, len(l)):
        if increasing:
            if l[i] < l[i-1]:
                return False
        elif decreasing:
            if l[i] > l[i-1]:
                return False
    
    return True