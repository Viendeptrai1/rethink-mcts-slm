import sys
import heapq

def main():
    import sys
    import heapq
    
    def readints():
        return list(map(int, sys.stdin.readline().split()))
    
    n, m, s = readints()
    a = readints()
    b = readints()
    c = readints()
    
    # Sort bugs by complexity in descending order
    a.sort(reverse=True)
    # Sort students by ability level in descending order
    students = sorted(zip(b, c), reverse=True)
    
    # Min-heap to keep track of the number of days each student will take
    heap = []
    # Dictionary to map each student to their index
    student_index = {ability: idx for idx, (ability, _) in enumerate(students)}
    
    # Assign bugs to students
    bug_assignments = [-1] * m
    total_passes = 0
    
    for bug_complexity in a:
        assigned = False
        for ability, cost in students:
            if ability >= bug_complexity:
                # Check if adding this student's cost exceeds the limit
                if total_passes + cost <= s:
                    total_passes += cost
                    bug_assignments.append(student_index[ability] + 1)
                    assigned = True
                    break
        if not assigned:
            print("NO")
            return
    
    print("YES")
    print(" ".join(map(str, bug_assignments)))

if __name__ == "__main__":
    main()