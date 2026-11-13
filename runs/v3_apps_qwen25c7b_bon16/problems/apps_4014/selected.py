def solve(n, m, exams):
    # Initialize the schedule with zeros
    schedule = [0] * n
    
    # Create a list of exam information
    exam_info = [(s_i, d_i, c_i) for s_i, d_i, c_i in exams]
    
    # Sort exams by the start day
    exam_info.sort()
    
    # Iterate over each day and assign activities
    for day in range(1, n + 1):
        # Check if today is an exam day
        for s_i, d_i, c_i in exam_info:
            if s_i <= day < d_i:
                if schedule[day - 1] == 0:
                    schedule[day - 1] = s_i
                    break
        
        # Check if there are exams that need preparation
        prepared = False
        for s_i, d_i, c_i in exam_info:
            if s_i <= day < d_i and schedule[day - 1] == s_i and day - s_i < c_i:
                schedule[day - 1] = s_i
                prepared = True
                break
        
        # Assign a rest day if no exam or preparation
        if not prepared and schedule[day - 1] == 0:
            schedule[day - 1] = m + 1
    
    # Check if all exams are passed and prepared
    for s_i, d_i, c_i in exam_info:
        if schedule[s_i - 1] != s_i or sum(1 for i in range(s_i, d_i) if schedule[i - 1] == s_i) != c_i:
            return -1
    
    return schedule

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
exams = []

for i in range(m):
    s_i = int(data[2 + i * 3])
    d_i = int(data[3 + i * 3])
    c_i = int(data[4 + i * 3])
    exams.append((s_i, d_i, c_i))

# Solve the problem
result = solve(n, m, exams)

# Print the result
if result == -1:
    print(-1)
else:
    print(' '.join(map(str, result)))