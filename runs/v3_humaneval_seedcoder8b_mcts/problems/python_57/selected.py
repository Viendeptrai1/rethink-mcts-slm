def monotonic(l: list):
    if len(l) <= 1:
        return True
    
    increasing = decreasing = True
    
    for i in range(1, len(l)):
        if l[i] < l[i-1]:
            increasing = False
        if l[i] > l[i-1]:
            decreasing = False
    
    return increasing or decreasing