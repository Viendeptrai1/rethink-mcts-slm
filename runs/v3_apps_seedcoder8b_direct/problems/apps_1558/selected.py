def min_essays_to_get_scholarship(n, r, avg, exams):
    current_sum = sum(a for a, b in exams)
    required_sum = avg * n
    if current_sum >= required_sum:
        return 0

    essays_needed = 0
    for a, b in exams:
        if current_sum < required_sum:
            increase = min(r - a, (required_sum - current_sum) // (n - exams.index((a, b))))
            essays_needed += increase * b
            current_sum += increase

    return essays_needed

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    r = int(data[1])
    avg = int(data[2])
    
    exams = []
    index = 3
    for _ in range(n):
        a_i = int(data[index])
        b_i = int(data[index + 1])
        exams.append((a_i, b_i))
        index += 2
    
    result = min_essays_to_get_scholarship(n, r, avg, exams)
    print(result)