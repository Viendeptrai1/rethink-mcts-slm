def monotonic(l: list):
    if len(l) <= 2:
        return True
    
    increasing = l[1] >= l[0]
    decreasing = l[1] <= l[0]
    
    for i in range(2, len(l)):
        if increasing:
            if l[i] < l[i-1]:
                return False
        elif decreasing:
            if l[i] > l[i-1]:
                return False
        else:
            # Mixed direction, e.g., [1, 2, 1] -> increasing was True, then l[2] < l[1] breaks it
            # But we need to check if it becomes strictly decreasing after being increasing?
            # Actually, the problem says "monotonically increasing OR decreasing"
            # So if we start increasing and then decrease, it's False.
            # If we start decreasing and then increase, it's False.
            # The only case where we switch is if the first two elements are equal.
            # Let's re-evaluate the logic.
            pass
    
    # Re-think: 
    # Monotonically increasing means: l[0] <= l[1] <= l[2] <= ...
    # Monotonically decreasing means: l[0] >= l[1] >= l[2] >= ...
    # So we just need to check one of these two conditions.
    
    increasing = True
    decreasing = True
    
    for i in range(1, len(l)):
        if l[i] < l[i-1]:
            increasing = False
        if l[i] > l[i-1]:
            decreasing = False
            
        if not increasing and not decreasing:
            return False
            
    return True