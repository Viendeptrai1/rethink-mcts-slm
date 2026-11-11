def solve(n, m, exams):
    from collections import defaultdict, deque
    
    # Create a graph where each exam is a node and edges represent feasible preparation days
    graph = defaultdict(list)
    for i in range(m):
        s_i, d_i, c_i = exams[i]
        for j in range(m):
            if i != j:
                s_j, d_j, c_j = exams[j]
                if d_i <= s_j:
                    graph[i].append(j)
    
    # Check if we can find a valid schedule using BFS
    def bfs():
        queue = deque([(None, [])])
        visited = set()
        
        while queue:
            current_exam, schedule = queue.popleft()
            
            if len(schedule) == m:
                return schedule
            
            for next_exam in range(m):
                if next_exam not in visited:
                    s_next, d_next, c_next = exams[next_exam]
                    if current_exam is None or d_exams[current_exam] <= s_next:
                        if len(schedule) == 0 or schedule[-1] != next_exam:
                            queue.append((next_exam, schedule + [next_exam]))
                            visited.add(next_exam)
        
        return None
    
    # Find a valid schedule
    schedule = bfs()
    if schedule is None:
        return [-1]
    
    # Create the final schedule array
    final_schedule = [0] * n
    for i in range(m):
        s_i, d_i, c_i = exams[i]
        for j in range(c_i):
            final_schedule[s_i + j] = i + 1
        final_schedule[d_i - 1] = m + 1
    
    return final_schedule

# Read input
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

# Solve the problem
result = solve(n, m, exams)

# Print the result
print(" ".join(map(str, result)))