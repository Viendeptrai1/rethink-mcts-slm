def min_day_to_take_final_exam(n, exams):
    exams.sort(key=lambda x: (x[1], x[0]))
    current_day = 0
    for a_i, b_i in exams:
        if current_day < b_i:
            current_day = b_i
        current_day += 1
    return current_day

if __name__ == "__main__":
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
    
    result = min_day_to_take_final_exam(n, exams)
    print(result)