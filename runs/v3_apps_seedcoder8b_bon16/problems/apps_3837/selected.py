def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    s = int(data[2])
    
    bugs = list(map(int, data[3:3 + m]))
    abilities = list(map(int, data[3 + m:3 + m + n]))
    passes_required = list(map(int, data[3 + m + n:3 + m + n + n]))
    
    # Create a list of (ability, passes, index) tuples for students and sort by ability in descending order
    students = sorted([(abilities[i], passes_required[i], i + 1) for i in range(n)], key=lambda x: -x[0])
    
    # Sort bugs by complexity in descending order
    bugs_with_index = sorted([(bugs[i], i + 1) for i in range(m)], key=lambda x: -x[0])
    
    # Prepare to allocate passes
    allocation = [-1] * m
    student_passes_used = [0] * n
    
    # Allocate students to bugs
    total_passes_used = 0
    for ability, required_passes, student_index in students:
        if total_passes_used + required_passes > s:
            continue
        for complexity, bug_index in bugs_with_index:
            if allocation[bug_index - 1] != -1:
                continue
            if ability >= complexity:
                allocation[bug_index - 1] = student_index
                student_passes_used[student_index - 1] += 1
                total_passes_used += 1
                if total_passes_used == s:
                    break
        if total_passes_used == s:
            break
    
    # Check if we managed to allocate all bugs
    if -1 in allocation:
        print("NO")
    else:
        print("YES")
        print(" ".join(map(str, allocation)))

main()