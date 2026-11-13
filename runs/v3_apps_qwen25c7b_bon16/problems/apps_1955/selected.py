from typing import List

def min_days_to_pass_exams(n: int, m: int, exams: List[int], prep_time: List[int]) -> int:
    if sum(exams) == 0:
        return -1
    
    max_prep = max(prep_time)
    total_prep_needed = sum(prep_time)
    
    if total_prep_needed > n:
        return -1
    
    days_used = 0
    exams_left = set(range(1, m + 1))
    
    for i in range(n):
        current_exam = exams[i]
        if current_exam != 0 and current_exam in exams_left:
            days_used += 1
            exams_left.remove(current_exam)
    
    return days_used + total_prep_needed - len(exams_left)

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    exams = list(map(int, data[2:n+2]))
    prep_time = list(map(int, data[n+2:]))
    
    result = min_days_to_pass_exams(n, m, exams, prep_time)
    print(result)