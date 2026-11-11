import sys
import heapq

def min_days_to_pass_exams(n, m, d, a):
    # Create a list of available days for each exam
    exam_days = [[] for _ in range(m + 1)]
    for i in range(n):
        if d[i] > 0:
            exam_days[d[i]].append(i)
    
    # Priority queue to store the next available day for each exam
    pq = []
    for i in range(1, m + 1):
        if len(exam_days[i]) == 0:
            return -1
        heapq.heappush(pq, (exam_days[i][0], i))
    
    # Dictionary to keep track of the last day Vasiliy prepared for each exam
    last_prepared = {i: -1 for i in range(1, m + 1)}
    
    current_day = 0
    
    while pq:
        next_exam_day, exam = heapq.heappop(pq)
        
        # Calculate the number of days needed to prepare for this exam
        prepare_days_needed = a[exam - 1]
        if last_prepared[exam] != -1:
            prepare_days_needed -= (next_exam_day - last_prepared[exam] - 1)
        
        if prepare_days_needed <= 0:
            # Vasiliy can take the exam on the next available day
            current_day = max(current_day, next_exam_day)
        else:
            # Vasiliy needs to prepare for the exam
            current_day = max(current_day, next_exam_day) + prepare_days_needed
        
        # Update the last prepared day for this exam
        last_prepared[exam] = current_day
        
        # Move to the next available day for this exam
        if len(exam_days[exam]) > 1:
            next_available_day = exam_days[exam].pop(0)
            heapq.heappush(pq, (next_available_day, exam))
    
    return current_day

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])

d = list(map(int, data[2:2+n]))
a = list(map(int, data[2+n:]))

# Output the result
print(min_days_to_pass_exams(n, m, d, a))