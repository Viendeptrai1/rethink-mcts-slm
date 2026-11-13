def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    
    exams = []
    index = 2
    for _ in range(m):
        s_i = int(data[index])
        d_i = int(data[index + 1])
        c_i = int(data[index + 2])
        exams.append((s_i, d_i, c_i))
        index += 3
    
    # Create a list to store the schedule
    schedule = [0] * n
    
    # Create a list to track preparation days for each exam
    preparation_days = [0] * m
    
    # Sort exams by their end day (d_i)
    exams = sorted(enumerate(exams), key=lambda x: x[1][1])
    
    # Try to schedule each exam
    for idx, (s_i, d_i, c_i) in exams:
        # Check if we have enough days to prepare for this exam
        available_days = 0
        for day in range(s_i, d_i):
            if schedule[day] == 0:
                available_days += 1
        
        if available_days < c_i:
            print(-1)
            return
        
        # Schedule preparation days
        current_day = s_i
        for _ in range(c_i):
            while schedule[current_day] != 0:
                current_day += 1
            schedule[current_day] = idx + 1
            preparation_days[idx] += 1
            current_day += 1
    
    # Schedule passing days
    for idx, (s_i, d_i, c_i) in exams:
        current_day = d_i
        while schedule[current_day] != 0:
            current_day += 1
        schedule[current_day] = m + 1
    
    # Output the schedule
    print(" ".join(map(str, schedule)))