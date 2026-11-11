import sys

def min_last_exam_day(n, exams):
    # Sort exams based on the schedule date a_i
    exams.sort(key=lambda x: x[0])
    
    # Initialize the current day to 0
    current_day = 0
    
    # Iterate through each exam
    for a_i, b_i in exams:
        # If we can take the exam on the early date without violating the order
        if b_i > current_day:
            current_day = b_i
        else:
            # Otherwise, we have to take it on the scheduled date
            current_day = a_i
    
    return current_day

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    exams = []
    
    index = 1
    for _ in range(n):
        a_i = int(data[index])
        b_i = int(data[index + 1])
        exams.append((a_i, b_i))
        index += 2
    
    result = min_last_exam_day(n, exams)
    print(result)

if __name__ == "__main__":
    main()