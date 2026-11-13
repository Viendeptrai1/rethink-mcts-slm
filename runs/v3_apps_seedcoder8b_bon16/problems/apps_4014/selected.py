def schedule_for_exams(n, m, exams):
    from collections import defaultdict, deque

    # Create a schedule array initialized with 0 (rest day)
    schedule = [0] * n

    # Create a list of preparation days for each exam
    prep_days = defaultdict(list)
    
    for i in range(m):
        s, d, c = exams[i]
        prep_days[i] = []

    # Attempt to schedule each exam
    for i in range(m):
        s, d, c = exams[i]

        # Try to fit the preparation and exam into the schedule
        prep_slots_needed = c
        current_day = s
        
        # Collect possible preparation days
        possible_prep_days = deque(range(s, d))

        while prep_slots_needed > 0 and possible_prep_days:
            day = possible_prep_days.popleft()
            if schedule[day - 1] == 0:  # Check if the day is a rest day
                prep_days[i].append(day)
                schedule[day - 1] = i + 1
                prep_slots_needed -= 1

        # If we couldn't fit all preparation days, return -1
        if prep_slots_needed > 0:
            return [-1]

        # Now, schedule the exam itself
        exam_day = d
        if schedule[exam_day - 1] == 0:  # Check if the exam day is a rest day
            schedule[exam_day - 1] = m + 1  # Marking it as exam day
        else:
            return [-1]  # Cannot schedule because it's not a rest day

    return schedule

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
m = int(data[1])
exams = []
index = 2
for _ in range(m):
    s = int(data[index])
    d = int(data[index+1])
    c = int(data[index+2])
    exams.append((s, d, c))
    index += 3

result = schedule_for_exams(n, m, exams)
print(" ".join(map(str, result)))