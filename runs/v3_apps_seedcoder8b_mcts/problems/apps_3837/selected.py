def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    s = int(data[2])
    
    a = list(map(int, data[3:3 + m]))
    b = list(map(int, data[3 + m:3 + m + n]))
    c = list(map(int, data[3 + m + n:3 + m + 2 * n]))
    
    # Create a list of students with their abilities and passes
    students = [(b[i], c[i], i + 1) for i in range(n)]
    
    # Sort bugs by complexity
    bugs = sorted((a[i], i + 1) for i in range(m))
    
    # Sort students by ability
    students.sort()
    
    # Result array to store which student fixes which bug
    result = [-1] * m
    
    # Total passes used
    total_passes_used = 0
    
    # Two pointers for bugs and students
    j = 0
    
    for ability, passes, student_index in students:
        while j < m and bugs[j][0] <= ability:
            result[bugs[j][1] - 1] = student_index
            total_passes_used += passes
            j += 1
        if j == m:
            break
    
    if total_passes_used > s:
        print("NO")
    else:
        print("YES")
        print(" ".join(map(str, result)))