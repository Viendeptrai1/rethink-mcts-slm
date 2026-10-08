def solve():
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
    
    # Check if it's possible to prepare for all exams
    for s_i, d_i, c_i in exams:
        if d_i - s_i - 1 < c_i:
            print(-1)
            return
    
    # Initialize the schedule
    schedule = [0] * n
    
    # Prepare for each exam
    for i in range(m):
        s_i, d_i, c_i = exams[i]
        prepared = 0
        for j in range(s_i, d_i):
            if prepared < c_i and schedule[j - 1] == 0:
                schedule[j - 1] = i + 1
                prepared += 1
    
    # Pass each exam
    for i in range(m):
        s_i, d_i, c_i = exams[i]
        schedule[d_i - 1] = m + 1
    
    print(" ".join(map(str, schedule)))

solve()