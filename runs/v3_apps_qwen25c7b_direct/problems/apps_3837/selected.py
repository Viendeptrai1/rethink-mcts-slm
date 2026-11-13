def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    s = int(data[2])
    
    a = list(map(int, data[3:3+m]))
    b = list(map(int, data[3+m:3+2*m]))
    c = list(map(int, data[3+2*m:]))
    
    # Sort students by their ability level
    students = sorted(range(n), key=lambda x: b[x], reverse=True)
    # Sort bugs by their complexity
    bugs = sorted(range(m), key=lambda x: a[x])
    
    # Initialize variables
    assigned_bugs = [-1] * m
    total_passes = 0
    
    # Assign bugs to students
    for bug in bugs:
        for student in students:
            if b[student] >= a[bug] and assigned_bugs[bug] == -1:
                assigned_bugs[bug] = student
                total_passes += c[student]
                break
    
    # Check if we can assign all bugs within the limit of passes
    if total_passes > s:
        print("NO")
    else:
        print("YES")
        print(' '.join(map(str, [assigned_bugs[i]+1 for i in range(m)])))

# Call the function to execute
solve()