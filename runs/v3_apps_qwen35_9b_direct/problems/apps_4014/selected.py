import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    iterator = iter(data)
    
    n = int(next(iterator))
    m = int(next(iterator))
    
    exams = []
    for i in range(m):
        s = int(next(iterator))
        d = int(next(iterator))
        c = int(next(iterator))
        exams.append({'id': i + 1, 's': s, 'd': d, 'c': c})
    
    # Sort exams by deadline (d_i)
    exams.sort(key=lambda x: x['d'])
    
    schedule = [0] * (n + 1)  # 1-based indexing for days
    
    # Track remaining preparation days needed for each exam
    remaining = {exam['id']: exam['c'] for exam in exams}
    
    # Track which exam is scheduled on which day (for output)
    # We will fill the schedule day by day from 1 to n
    
    # First, mark exam days as (m+1)
    exam_days_map = {}
    for exam in exams:
        exam_days_map[exam['d']] = exam['id']
    
    for day in range(1, n + 1):
        if day in exam_days_map:
            exam_id = exam_days_map[day]
            schedule[day] = m + 1
            continue
        
        # Try to find an exam that needs preparation and can be prepared today
        # An exam i can be prepared on day 'day' if:
        # 1. remaining[i] > 0
        # 2. day >= s_i
        # 3. day < d_i
        # 4. We prioritize exams with earlier deadlines to avoid missing them
        
        best_exam = -1
        min_deadline = float('inf')
        
        for exam in exams:
            eid = exam['id']
            if remaining[eid] > 0 and day >= exam['s'] and day < exam['d']:
                if exam['d'] < min_deadline:
                    min_deadline = exam['d']
                    best_exam = eid
        
        if best_exam != -1:
            schedule[day] = best_exam
            remaining[best_exam] -= 1
        else:
            # If no exam can be prepared today, it must be a rest day
            schedule[day] = 0
    
    # Check if all exams are fully prepared
    possible = True
    for exam in exams:
        if remaining[exam['id']] > 0:
            possible = False
            break
    
    if not possible:
        print("-1")
    else:
        # Output schedule from day 1 to n
        print(*(schedule[1:]))

if __name__ == "__main__":
    solve()