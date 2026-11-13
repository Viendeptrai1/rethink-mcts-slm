def min_last_exam_day(n, exams):
    exams.sort(key=lambda x: x[1])
    max_day = 0
    for a, b in exams:
        max_day = max(max_day, b)
    return max_day

# Example usage:
n = int(input())
exams = [tuple(map(int, input().split())) for _ in range(n)]
print(min_last_exam_day(n, exams))