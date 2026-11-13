def find_schedule(n, m, exams):
    # Initialize the schedule with zeros
    schedule = [0] * n
    
    # Sort exams based on the start day
    exams.sort(key=lambda x: x[0])
    
    # Dictionary to keep track of available preparation slots
    prep_slots = {i: [] for i in range(1, m+1)}
    
    # Try to place exams and their preparation slots
    for s, d, c in exams:
        # Find a slot for the exam
        found_slot = False
        for i in range(s, d):
            if len(prep_slots[i]) < c:
                prep_slots[i].append(i)
                schedule[i-1] = s + prep_slots[i].index(i) + 1
                found_slot = True
                break
        
        # If no slot is found, return -1
        if not found_slot:
            return -1
    
    # Fill the remaining days with rests
    for i in range(n):
        if schedule[i] == 0:
            schedule[i] = 0
    
    return schedule

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])

exams = []
for i in range(m):
    s = int(data[2 + 3*i])
    d = int(data[3 + 3*i])
    c = int(data[4 + 3*i])
    exams.append((s, d, c))

# Find and print the schedule
result = find_schedule(n, m, exams)
if result == -1:
    print(-1)
else:
    print(' '.join(map(str, result)))