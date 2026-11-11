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
    
    # Initialize the schedule with zeros
    schedule = [0] * n
    
    # Try to assign preparation days
    for i in range(m):
        s_i, d_i, c_i = exams[i]
        prepared_days = 0
        for j in range(s_i, d_i):
            if schedule[j - 1] == 0:
                schedule[j - 1] = i + 1
                prepared_days += 1
                if prepared_days == c_i:
                    break
        if prepared_days != c_i:
            print(-1)
            return
    
    # Assign exam days
    for i in range(m):
        s_i, d_i, c_i = exams[i]
        schedule[d_i - 1] = m + 1
    
    print(" ".join(map(str, schedule)))

solve()