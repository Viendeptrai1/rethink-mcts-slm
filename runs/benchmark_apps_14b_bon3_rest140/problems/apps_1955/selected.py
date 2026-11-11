import sys
import heapq

def min_days_to_pass_exams(n, m, d, a):
    # Create a list of available days for each exam
    exam_days = [[] for _ in range(m + 1)]
    for i in range(n):
        if d[i] != 0:
            exam_days[d[i]].append(i)
    
    # Priority queue to store the next available day to take each exam
    pq = []
    for i in range(1, m + 1):
        if len(exam_days[i]) > 0:
            heapq.heappush(pq, (exam_days[i][0], i))
        else:
            return -1
    
    # Array to keep track of the last day Vasiliy prepared for each exam
    last_prepared = [-1] * (m + 1)
    
    # Variable to keep track of the current day
    current_day = 0
    
    while pq:
        # Get the exam with the next available day
        next_day, exam = heapq.heappop(pq)
        
        # Calculate the number of days needed to prepare for this exam
        if last_prepared[exam] == -1:
            prepare_days = a[exam - 1]
        else:
            prepare_days = max(0, a[exam - 1] - (next_day - last_prepared[exam] - 1))
        
        # Check if there are enough days left to prepare and take the exam
        if next_day + prepare_days >= n:
            return -1
        
        # Update the current day
        current_day = next_day + prepare_days
        
        # Mark the last day Vasiliy prepared for this exam
        last_prepared[exam] = current_day
        
        # Find the next available day to take this exam
        next_exam_day_index = bisect.bisect_right(exam_days[exam], current_day)
        if next_exam_day_index < len(exam_days[exam]):
            next_exam_day = exam_days[exam][next_exam_day_index]
            heapq.heappush(pq, (next_exam_day, exam))
    
    return current_day + 1

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
m = int(data[1])
d = list(map(int, data[2:2+n]))
a = list(map(int, data[2+n:2+n+m]))

# Output the result
print(min_days_to_pass_exams(n, m, d, a))