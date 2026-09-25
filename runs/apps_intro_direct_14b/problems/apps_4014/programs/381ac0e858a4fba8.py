import sys
from typing import List

def can_pass_exams(n: int, m: int, exams: List[List[int]]) -> List[int]:
    # Initialize the schedule with zeros (rest days)
    schedule = [0] * n
    
    # Sort exams by their exam day
    exams.sort(key=lambda x: x[1])
    
    # Try to assign preparation days for each exam
    for s, d, c in exams:
        # Find available days for preparation
        available_days = [i for i in range(s, d) if schedule[i] == 0]
        
        # Check if we have enough days to prepare
        if len(available_days) < c:
            return [-1]
        
        # Assign preparation days
        for i in range(c):
            schedule[available_days[i]] = exams.index([s, d, c]) + 1
    
    # Assign exam days
    for i, (s, d, c) in enumerate(exams):
        schedule[d - 1] = m + 1
    
    return schedule

def main():
    import sys
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
    
    result = can_pass_exams(n, m, exams)
    
    if result == [-1]:
        print(-1)
    else:
        print(" ".join(map(str, result)))

if __name__ == "__main__":
    main()