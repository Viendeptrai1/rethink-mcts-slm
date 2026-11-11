import sys
import heapq

def main():
    import sys
    import heapq
    
    def readints():
        return list(map(int, sys.stdin.readline().split()))
    
    n, m, s = readints()
    bugs = readints()
    students_abilities = readints()
    students_passes = readints()
    
    # Sort bugs by complexity
    bugs.sort()
    # Sort students by ability, and then by passes (to prioritize those who ask for fewer passes)
    students = sorted(zip(students_abilities, students_passes), reverse=True)
    
    # Min-heap to keep track of the days each student will be free
    min_heap = []
    for i, (ability, passes) in enumerate(students):
        heapq.heappush(min_heap, (0, i))  # (day, student_index)
    
    total_passes = 0
    assignment = [-1] * m
    
    for bug in bugs:
        while min_heap and students[min_heap[0][1]][0] < bug:
            heapq.heappop(min_heap)
        
        if not min_heap:
            print("NO")
            return
        
        day, student_index = heapq.heappop(min_heap)
        assignment[bugs.index(bug)] = student_index + 1
        total_passes += students[student_index][1]
        
        if total_passes > s:
            print("NO")
            return
        
        # Push the student back into the heap with the next available day
        heapq.heappush(min_heap, (day + 1, student_index))
    
    print("YES")
    print(" ".join(map(str, assignment)))

if __name__ == "__main__":
    main()