import sys
from collections import defaultdict

def main():
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
    
    # Initialize the schedule array
    schedule = [0] * n
    
    # Check if it's possible to prepare and pass all exams
    for i in range(m):
        s_i, d_i, c_i = exams[i]
        
        # Check if there are enough days to prepare for the exam
        if d_i - s_i - 1 < c_i:
            print(-1)
            return
        
        # Mark the exam day
        schedule[d_i - 1] = m + 1
    
    # Prepare for exams
    for i in range(m):
        s_i, d_i, c_i = exams[i]
        prepared_days = 0
        
        for j in range(s_i, d_i):
            if schedule[j - 1] == 0:
                schedule[j - 1] = i + 1
                prepared_days += 1
                if prepared_days == c_i:
                    break
    
    # Print the schedule
    print(" ".join(map(str, schedule)))

if __name__ == "__main__":
    main()