def max_students_to_lunch():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    group_sizes = list(map(int, data[1:n+1]))
    k = int(data[n+1])
    x = int(data[n+2])
    a = int(data[n+3])
    b = int(data[n+4])
    
    total_students = sum(group_sizes)
    max_possible = min(total_students, b)
    min_required = a
    
    if max_possible < min_required:
        return 'impossible'
    
    # Check each possible number of students from min_required to max_possible
    for num_students in range(max_possible, min_required - 1, -1):
        if num_students % x == 0 and num_students >= min_required and num_students <= max_possible:
            return num_students

# Call the function and print the result
print(max_students_to_lunch())