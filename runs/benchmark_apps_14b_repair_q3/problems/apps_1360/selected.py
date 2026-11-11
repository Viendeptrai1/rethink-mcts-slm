import sys

def min_last_exam_day(n, exams):
    exams.sort(key=lambda x: (x[0], -x[1]))
    current_day = 0
    for a, b in exams:
        if b > current_day:
            current_day = b
        else:
            current_day = a
    return current_day

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    exams = []
    index = 1
    for _ in range(n):
        a = int(data[index])
        b = int(data[index + 1])
        exams.append((a, b))
        index += 2
    
    result = min_last_exam_day(n, exams)
    print(result)

if __name__ == "__main__":
    main()