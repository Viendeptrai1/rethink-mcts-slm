from typing import List

def min_last_exam_day(n: int, exams: List[List[int]]) -> int:
    exams.sort(key=lambda x: (x[1], -x[0]))
    return max(a for _, a in exams)

# Input handling
n = int(input())
exams = [list(map(int, input().split())) for _ in range(n)]

# Output the result
print(min_last_exam_day(n, exams))