import sys
from typing import List

def find_schedule(n: int, m: int, exams: List[List[int]]) -> List[int]:
    # Sort exams by the day they need to be passed
    exams.sort(key=lambda x: x[1])
    
    # Initialize the schedule with zeros
    schedule = [0] * n
    
    # Dictionary to keep track of preparation days used for each exam
    prep_days_used = {i+1: 0 for i in range(m)}
    
    for i in range(m):
        s, d, c = exams[i]
        
        # Try to find available days for preparation
        for j in range(s, d):
            if prep_days_used[i+1] < c and schedule[j] == 0:
                schedule[j] = i + 1
                prep_days_used[i+1] += 1
        
        # Check if we can pass the exam on its due date
        if schedule[d-1] != 0:
            return [-1]
        
        # Pass the exam on its due date
        schedule[d-1] = m + 1
    
    return schedule

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])

exams = []
index = 2
for _ in range(m):
    s = int(data[index])
    d = int(data[index + 1])
    c = int(data[index + 2])
    exams.append([s, d, c])
    index += 3

# Find and print the schedule
result = find_schedule(n, m, exams)
print(" ".join(map(str, result)))