import sys
import heapq

def min_days_to_pass_exams(n, m, d, a):
    # Create a list of available days for each exam
    exam_days = [[] for _ in range(m + 1)]
    for i in range(n):
        if d[i] > 0:
            exam_days[d[i]].append(i)
    
    # Priority queue to store the earliest available day for each exam
    pq = []
    for i in range(1, m + 1):
        if len(exam_days[i]) > 0:
            heapq.heappush(pq, (exam_days[i][0], i))
    
    # Array to keep track of the last day Vasiliy prepared for each exam
    last_prepared = [-1] * (m + 1)
    
    # Variable to count the total number of days used
    total_days = 0
    
    while pq:
        day, exam = heapq.heappop(pq)
        
        # Calculate the number of days needed to prepare for this exam
        if last_prepared[exam] == -1:
            prepare_days = a[exam - 1]
        else:
            prepare_days = max(0, a[exam - 1] - (day - last_prepared[exam]))
        
        # Check if there are enough days left to prepare and take the exam
        if day + prepare_days >= n:
            return -1
        
        # Update the last prepared day for this exam
        last_prepared[exam] = day + prepare_days
        
        # Increment the total number of days used
        total_days = max(total_days, day + prepare_days + 1)
        
        # Move to the next available day for this exam
        if len(exam_days[exam]) > 1:
            next_day = exam_days[exam].pop(0)
            heapq.heappush(pq, (next_day, exam))
    
    return total_days

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
m = int(data[1])
d = list(map(int, data[2:2+n]))
a = list(map(int, data[2+n:2+n+m]))

# Output the result
print(min_days_to_pass_exams(n, m, d, a))