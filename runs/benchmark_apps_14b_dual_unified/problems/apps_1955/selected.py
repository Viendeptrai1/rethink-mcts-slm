import sys
from collections import defaultdict

def min_days_to_pass_exams(n, m, d, a):
    # Dictionary to store the days when each exam can be taken
    exam_days = defaultdict(list)
    for i in range(n):
        if d[i] != 0:
            exam_days[d[i]].append(i)
    
    # Check if it's possible to take all exams
    for i in range(1, m + 1):
        if len(exam_days[i]) == 0:
            return -1
    
    # Sort the days for each exam
    for i in range(1, m + 1):
        exam_days[i].sort()
    
    # Priority queue to store the next available day to take an exam
    import heapq
    pq = []
    for i in range(1, m + 1):
        heapq.heappush(pq, (exam_days[i][0], i))
    
    # Dictionary to store the last day Vasiliy prepared for each exam
    last_prepared = {i: -1 for i in range(1, m + 1)}
    
    # Variable to store the current day
    current_day = 0
    
    while pq:
        # Get the exam with the next available day to take
        next_exam_day, exam_id = heapq.heappop(pq)
        
        # Calculate the number of days needed to prepare for this exam
        if last_prepared[exam_id] != -1:
            prepare_days_needed = max(0, exam_days[exam_id][0] - last_prepared[exam_id] - 1)
        else:
            prepare_days_needed = max(0, exam_days[exam_id][0] - a[exam_id - 1])
        
        # Update the current day
        current_day = max(current_day, next_exam_day)
        
        # Check if there is enough time to prepare for the exam
        if current_day + prepare_days_needed >= exam_days[exam_id][0]:
            # Update the last prepared day for this exam
            last_prepared[exam_id] = exam_days[exam_id][0] - 1
            
            # Move to the next day to take the exam
            current_day = exam_days[exam_id][0]
            
            # Remove the taken exam day from the list
            exam_days[exam_id].pop(0)
            
            # If there are more days left for this exam, push the next available day to the priority queue
            if exam_days[exam_id]:
                heapq.heappush(pq, (exam_days[exam_id][0], exam_id))
        else:
            # If there is not enough time to prepare, push the same exam back to the priority queue
            heapq.heappush(pq, (next_exam_day, exam_id))
    
    return current_day

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])

d = [int(x) for x in data[2:2+n]]
a = [int(x) for x in data[2+n:]]

# Output the result
print(min_days_to_pass_exams(n, m, d, a))