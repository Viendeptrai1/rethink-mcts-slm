import sys

def main():
    import sys
    import heapq
    
    def readints():
        return list(map(int, sys.stdin.readline().split()))
    
    n, r, avg = readints()
    exams = [readints() for _ in range(n)]
    
    # Calculate the total number of essays needed to reach the required average
    total_required_grade = n * avg
    current_total_grade = sum(a for a, b in exams)
    additional_grade_needed = max(0, total_required_grade - current_total_grade)
    
    # If no additional grade is needed, Vanya doesn't need to write any essays
    if additional_grade_needed == 0:
        print(0)
        return
    
    # Create a min-heap based on the number of essays needed per grade point increase
    heap = []
    for a, b in exams:
        if a < r:
            heapq.heappush(heap, (b, a))
    
    # Calculate the minimum number of essays needed
    essays_needed = 0
    while heap and additional_grade_needed > 0:
        b, a = heapq.heappop(heap)
        max_increase = min(r - a, additional_grade_needed)
        essays_needed += max_increase * b
        additional_grade_needed -= max_increase
    
    # If it's still not possible to reach the required average, print -1
    if additional_grade_needed > 0:
        print(-1)
    else:
        print(essays_needed)

if __name__ == "__main__":
    main()