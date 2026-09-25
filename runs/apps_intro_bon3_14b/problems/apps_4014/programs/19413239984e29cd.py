import sys

def main():
    import sys
    import heapq
    
    def can_pass_exams(n, m, exams):
        # Create a list of events: (day, type, exam_index)
        events = []
        for i, (s, d, c) in enumerate(exams):
            events.append((s, 'start', i))
            events.append((d, 'end', i))
        
        # Sort events by day
        events.sort()
        
        # Priority queue to keep track of ongoing preparations
        pq = []
        # Array to store the schedule
        schedule = [0] * n
        
        for day, event_type, exam_index in events:
            if event_type == 'start':
                # Check if we can start preparing for this exam
                if len(pq) + sum(1 for x in schedule if x == exam_index + 1) >= c:
                    return -1
                # Mark the day as preparation day
                schedule[day - 1] = exam_index + 1
                # Add to priority queue
                heapq.heappush(pq, (day + c, exam_index))
            else:
                # End of preparation for this exam
                while pq and pq[0][0] <= day:
                    heapq.heappop(pq)
        
        # Fill remaining days with rest
        for i in range(n):
            if schedule[i] == 0:
                schedule[i] = m + 1
        
        return schedule
    
    # Read input
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    n = int(data[index])
    m = int(data[index + 1])
    index += 2
    
    exams = []
    for _ in range(m):
        s = int(data[index])
        d = int(data[index + 1])
        c = int(data[index + 2])
        exams.append((s, d, c))
        index += 3
    
    # Solve the problem
    result = can_pass_exams(n, m, exams)
    
    # Print the result
    if result == -1:
        print(-1)
    else:
        print(' '.join(map(str, result)))

if __name__ == "__main__":
    main()