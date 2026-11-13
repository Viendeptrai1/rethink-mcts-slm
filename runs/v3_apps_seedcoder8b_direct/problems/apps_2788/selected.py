def max_students_for_lunch():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    group_sizes = list(map(int, data[1:n+1]))
    k, x, a, b = map(int, data[n+1:n+5])
    
    total_students = sum(group_sizes)
    total_lunches = k * x
    
    # If total students are less than the minimum campers to watch, it's impossible
    if total_students < a:
        print("impossible")
        return
    
    # Calculate the maximum number of students we can take to lunch
    # We need to ensure we don't exceed the total number of available lunches
    max_students = min(total_students, total_lunches)
    
    # Ensure we don't watch more campers than allowed
    if max_students > b:
        max_students = b
    
    # Ensure we take at least 'a' students
    if max_students < a:
        print("impossible")
        return
    
    print(max_students)