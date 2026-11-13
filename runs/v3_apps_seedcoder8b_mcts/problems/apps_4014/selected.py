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
    
    # Sort exams by their end day (d_i)
    exams.sort(key=lambda x: x[1])
    
    # Initialize the schedule with zeroes (rest days)
    schedule = [0] * n
    
    # Track preparation days for each exam
    preparation_days = [0] * m
    
    # Try to schedule each exam
    for i, (s_i, d_i, c_i) in enumerate(exams):
        # Find a block of c_i days to prepare for the exam
        prepared = False
        for start in range(s_i, d_i - c_i + 1):
            if all(schedule[j] == 0 for j in range(start, start + c_i)):
                # Mark these days as preparation for exam i+1
                for j in range(start, start + c_i):
                    schedule[j] = i + 1
                preparation_days[i] = c_i
                prepared = True
                break
        
        if not prepared:
            print(-1)
            return
    
    # Now, fill in the remaining days with exams and rest days
    exam_index = 0
    for day in range(n):
        if schedule[day] == 0:
            # If there's an exam on this day, mark it
            if exam_index < m and day + 1 == exams[exam_index][1]:
                schedule[day] = m + 1
                exam_index += 1
    
    # Print the schedule
    print(" ".join(map(str, schedule)))