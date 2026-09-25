import sys
from collections import deque

def max_students_in_teams(n, k, skills):
    skills.sort()
    max_students = 0
    queue = deque()
    
    for skill in skills:
        while queue and skill - queue[0] > 5:
            queue.popleft()
        queue.append(skill)
        if len(queue) > max_students:
            max_students = len(queue)
    
    return max_students

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    skills = list(map(int, data[2:]))
    
    result = max_students_in_teams(n, k, skills)
    print(result)

if __name__ == "__main__":
    main()