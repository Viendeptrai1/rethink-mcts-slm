def min_last_exam_day(n, exams):
    exams.sort(key=lambda x: x[1])
    current_day = 0
    for _, a_i in exams:
        current_day = max(current_day + 1, a_i)
    return current_day

# Example usage:
n = int(input())
exams = [tuple(map(int, input().split())) for _ in range(n)]
print(min_last_exam_day(n, exams))